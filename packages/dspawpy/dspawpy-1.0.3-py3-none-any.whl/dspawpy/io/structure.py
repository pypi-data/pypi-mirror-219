# -*- coding: utf-8 -*-
import os
import re
import warnings
from typing import List, Union

import numpy as np
from dspawpy.io.read import get_lines_without_comment, get_sinfo
from dspawpy.io.utils import get_absfile
from pymatgen.core import Structure


def build_Structures_from_datafile(
    datafile: Union[str, List[str]], si=None, ele=None, ai=None, fmt=None, task="scf"
) -> List[Structure]:
    r"""读取一/多个h5/json文件，返回pymatgen的Structures列表

    Parameters
    ----------
    datafile : str or list
        - h5/json/as/hzw/cif/poscar/cssr/xsf/mcsqs/prismatic/yaml/fleur-inpgen文件路径;
        - 若给定文件夹路径，可配合task参数读取内部的 {task}.h5/json 文件
        - 若给定字符串列表，将依次读取数据并合并成一个Structures列表
    si: int, list or str
        - 构型编号，从 1 开始

            - si=1, 读取第一个构型
            - si=[1,2], 读取第一个和第二个构型
            - si=':', 读取所有构型
            - si='-3:', 读取最后三个构型
        - 若为空，多构型文件将读取所有构型，单构型文件将读取最新构型
        - 此参数仅对 h5/json 文件有效
    ele: str or list
        - 元素符号，写法参考：'H' 或 ['H','O']
        - 若为空，将读取所有元素的原子信息
        - 此参数仅对 h5/json 文件有效
    ai: int or list or str
        - 原子编号，从 1 开始
        - 用法同si
        - 若为空，将读取所有原子信息
        - 此参数仅对 h5/json 文件有效
    fmt: str
        - 文件格式，包括 'h5', 'json', 'as', 'hzw' 四种，其他值将被忽略。
        - 若为空，文件类型将依据文件名称惯例判断。
    task: str
        - 用于当 datafile 为文件夹路径时，寻找内部的 {task}.h5/json 文件。
        - 计算任务类型，包括 'scf', 'relax', 'neb', 'aimd' 四种，其他值将被忽略。

    Returns
    -------
    pymatgen_Structures : List[Structure]
        结构列表

    Examples
    --------

    >>> from dspawpy.io.structure import build_Structures_from_datafile as bs

    读取单个文件生成 Structures 列表，支持四种类型

    >>> pymatgen_Structures = bs(datafile='/data/home/hzw1002/dspawpy_repo/test/2.1/relax.h5')
    Reading /data/home/hzw1002/dspawpy_repo/test/2.1/relax.h5...
    >>> len(pymatgen_Structures)
    3
    >>> pymatgen_Structures = bs(datafile='/data/home/hzw1002/dspawpy_repo/test/2.1/relax.json')
    Reading /data/home/hzw1002/dspawpy_repo/test/2.1/relax.json...
    >>> len(pymatgen_Structures)
    3
    >>> pymatgen_Structures = bs(datafile='/data/home/hzw1002/dspawpy_repo/test/supplement/PtH.as')
    >>> len(pymatgen_Structures)
    1
    >>> pymatgen_Structures = bs(datafile='/data/home/hzw1002/dspawpy_repo/test/supplement/PtH.hzw')
    >>> len(pymatgen_Structures)
    1

    注意pymatgen_Structures是由多个 Structure 对象组成的列表，每个 Structure 对象分别对应一个构型。如果只有一个构型，也会返回列表，请使用 pymatgen_Structures[0] 获取 Structure 对象

    当datafile为列表时，将依次读取多个文件，合并成一个Structures列表

    >>> pymatgen_Structures = bs(datafile=['/data/home/hzw1002/dspawpy_repo/test/supplement/aimd1.h5','/data/home/hzw1002/dspawpy_repo/test/supplement/aimd2.h5'])
    Reading /data/home/hzw1002/dspawpy_repo/test/supplement/aimd1.h5...
    Reading /data/home/hzw1002/dspawpy_repo/test/supplement/aimd2.h5...
    """
    dfs = []
    if isinstance(datafile, list):  # 续算模式，给的是多个文件
        dfs = datafile
    else:  # 单次计算模式，处理单个文件
        dfs.append(datafile)

    # 读取结构数据
    pymatgen_Structures = []
    for df in dfs:
        structure_list = _get_structure_list(df, si, ele, ai, fmt, task)
        pymatgen_Structures.extend(structure_list)

    return pymatgen_Structures


def _get_structure_list(
    df: str, si=None, ele=None, ai=None, fmt=None, task="scf"
) -> List[Structure]:
    """get pymatgen structures from single datafile

    Parameters
    ----------
    df : str
        数据文件路径或包含数据文件的文件夹路径

    Returns
    -------
    List[Structure] : list of pymatgen structures
    """
    if task is None:
        task = "scf"

    if os.path.isdir(df) or df.endswith(".h5") or df.endswith(".json"):
        absfile = get_absfile(df, task=task)
    else:  # for other type of datafile, such as .as, .hzw, POSCAR
        absfile = os.path.abspath(df)

    if fmt is None:
        fmt = absfile.split(".")[-1]
    else:
        assert isinstance(fmt, str), "fmt must be str"

    if fmt == "as":
        strs = [_from_dspaw_as(absfile)]
    elif fmt == "hzw":
        warnings.warn("build from .hzw may lack mag & fix info!", category=UserWarning)
        strs = [_from_hzw(absfile)]
    elif fmt == "h5" or fmt == "json":
        Nstep, elements, positions, lattices, D_mag_fix = get_sinfo(
            datafile=absfile, si=si, ele=ele, ai=ai
        )  # returned positions, not scaled-positions
        # remove _ from elements
        elements = [re.sub(r"_", "", e) for e in elements]

        strs = []
        for i in range(Nstep):
            if D_mag_fix:
                strs.append(
                    Structure(
                        lattices[i],
                        elements,
                        positions[i],
                        coords_are_cartesian=True,
                        site_properties={k: v[i] for k, v in D_mag_fix.items()},
                    )
                )
            else:
                strs.append(
                    Structure(
                        lattices[i],
                        elements,
                        positions[i],
                        coords_are_cartesian=True,
                    )
                )
    else:
        strs = [Structure.from_file(absfile)]

    return strs


def _from_dspaw_as(as_file: str = "structure.as") -> Structure:
    """从DSPAW的as结构文件中读取结构信息

    Parameters
    ----------
    as_file : str
        DSPAW的as结构文件, 默认'structure.as'

    Returns
    -------
    Structure
        pymatgen的Structure对象
    """
    absfile = os.path.abspath(as_file)
    lines = get_lines_without_comment(absfile, "#")
    N = int(lines[1])  # number of atoms

    # parse lattice info
    lattice = []  # lattice matrix
    for line in lines[3:6]:
        vector = line.split()
        lattice.extend([float(vector[0]), float(vector[1]), float(vector[2])])
    lattice = np.asarray(lattice).reshape(3, 3)

    lat_fixs = []
    if lines[2].strip() != "Lattice":  # fix lattice
        lattice_fix_info = lines[2].strip().split()[1:]
        if lattice_fix_info == ["Fix_x", "Fix_y", "Fix_z"]:
            # ONLY support xyz fix in sequence, yzx will cause error
            for line in lines[3:6]:
                lfs = line.strip().split()[3:6]
                for lf in lfs:
                    if lf.startswith("T"):
                        lat_fixs.append("True")
                    elif lf.startswith("F"):
                        lat_fixs.append("False")
        elif lattice_fix_info == ["Fix"]:
            for line in lines[3:6]:
                lf = line.strip().split()[3]
                if lf.startswith("T"):
                    lat_fixs.append("True")
                elif lf.startswith("F"):
                    lat_fixs.append("False")
        else:
            raise ValueError("Lattice fix info error!")

    elements = []
    positions = []
    for i in range(N):
        atom = lines[i + 7].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]), float(atom[2]), float(atom[3])])

    mf_info = None
    l6 = lines[6].strip()  # str, 'Cartesian/Direct Mag Fix_x ...'
    if l6.split()[0] == "Direct":
        is_direct = True
    elif l6.split()[0] == "Cartesian":
        is_direct = False
    else:
        raise ValueError("Structure file format error!")

    mf_info = l6.split()[1:]  # ['Mag', 'Fix_x', 'Fix_y', 'Fix_z']
    for item in mf_info:
        assert item in [
            "Mag",
            "Mag_x",
            "Mag_y",
            "Mag_z",
            "Fix",
            "Fix_x",
            "Fix_y",
            "Fix_z",
        ], "Mag/Fix info error!"

    mag_fix_dict = {}
    if mf_info is not None:
        for mf_index, item in enumerate(mf_info):
            values = []
            for i in range(N):
                atom = lines[i + 7].strip().split()
                mf = atom[4:]
                values.append(mf[mf_index])

            if item.startswith("Fix"):  # F -> False, T -> True
                for value in values:
                    if value.startswith("T"):
                        values[values.index(value)] = "True"
                    elif value.startswith("F"):
                        values[values.index(value)] = "False"
            mag_fix_dict[item] = values

    if lat_fixs != []:
        # replicate lat_fixs to N atoms
        mag_fix_dict["LatticeFixs"] = [lat_fixs for i in range(N)]

    coords = np.asarray(positions).reshape(-1, 3)
    # remove _ from elements
    elements = [re.sub(r"_", "", e) for e in elements]

    if mag_fix_dict == {}:
        return Structure(
            lattice, elements, coords, coords_are_cartesian=(not is_direct)
        )
    else:
        return Structure(
            lattice,
            elements,
            coords,
            coords_are_cartesian=(not is_direct),
            site_properties=mag_fix_dict,
        )


def _from_hzw(hzw_file) -> Structure:
    """从hzw结构文件中读取结构信息

    Parameters
    ----------
    hzw_file : str
        hzw结构文件，以 .hzw 结尾

    Returns
    -------
    Structure
        pymatgen的Structure对象
    """
    absfile = os.path.abspath(hzw_file)
    lines = get_lines_without_comment(absfile, "%")
    number_of_probes = int(lines[0])
    if number_of_probes != 0:
        raise ValueError("dspaw only support 0 probes hzw file")
    lattice = []
    for line in lines[1:4]:
        vector = line.split()
        lattice.extend([float(vector[0]), float(vector[1]), float(vector[2])])

    lattice = np.asarray(lattice).reshape(3, 3)
    N = int(lines[4])
    elements = []
    positions = []
    for i in range(N):
        atom = lines[i + 5].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]), float(atom[2]), float(atom[3])])

    coords = np.asarray(positions).reshape(-1, 3)
    return Structure(lattice, elements, coords, coords_are_cartesian=True)

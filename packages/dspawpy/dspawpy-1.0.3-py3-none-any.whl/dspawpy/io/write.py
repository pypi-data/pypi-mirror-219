# -*- coding: utf-8 -*-
import json
import os
import time
import warnings

import numpy as np
from dspawpy.io.read import _get_lammps_non_orthogonal_box, load_h5
from dspawpy.io.structure import build_Structures_from_datafile
from dspawpy.io.utils import _symbols2numbers
from pymatgen.core.structure import Structure

Bohr = 0.52917721067  # Angstrom


def _write_xyz_traj(
    structures,
    xyzfile="aimdTraj.xyz",
):
    r"""保存xyz格式的轨迹文件

    Parameters
    ----------
    structures: list
        pymatgen的Structures列表
    xyzfile : str
        写入xyz格式的轨迹文件，默认为aimdTraj.xyz
    """
    if not isinstance(structures, list):  # single Structure
        structures = [structures]
    if xyzfile is not None:
        absxyz = os.path.abspath(xyzfile)
    if os.path.isfile(absxyz):
        warnings.warn(
            f"{absxyz} already exists and will be overwritten!", category=UserWarning
        )
    os.makedirs(os.path.dirname(absxyz), exist_ok=True)
    with open(absxyz, "w") as f:
        # Nstep
        for _, structure in enumerate(structures):
            # 原子数不会变，就是不合并的元素总数
            eles = [s.species_string for s in structure.sites]
            f.write("%d\n" % len(eles))
            # lattice
            lm = structure.lattice.matrix
            f.write(
                'Lattice="%f %f %f %f %f %f %f %f %f" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                % (
                    lm[0, 0],
                    lm[0, 1],
                    lm[0, 2],
                    lm[1, 0],
                    lm[1, 1],
                    lm[1, 2],
                    lm[2, 0],
                    lm[2, 1],
                    lm[2, 2],
                )
            )
            # position and element
            poses = structure.cart_coords
            for j in range(len(eles)):
                f.write(
                    "%s %f %f %f\n" % (eles[j], poses[j, 0], poses[j, 1], poses[j, 2])
                )

    print(f"==> {absxyz}")


def _write_dump_traj(
    structures,
    dumpfile="aimdTraj.dump",
):
    r"""保存为lammps的dump格式的轨迹文件，暂时只支持正交晶胞

    Parameters
    ----------
    structures: list
        pymatgen的Structures列表
    dumpfile : str
        dump格式的轨迹文件名，默认为aimdTraj.dump
    """
    if not isinstance(structures, list):  # single Structure
        structures = [structures]
    if dumpfile is not None:
        absdump = os.path.abspath(dumpfile)
    if os.path.isfile(absdump):
        warnings.warn(f"{absdump} already exists and will be overwritten!")
    os.makedirs(os.path.dirname(absdump), exist_ok=True)
    with open(absdump, "w") as f:
        for n, structure in enumerate(structures):
            lat = structure.lattice.matrix
            eles = [s.species_string for s in structure.sites]
            poses = structure.cart_coords

            box_bounds = _get_lammps_non_orthogonal_box(lat)
            f.write("ITEM: TIMESTEP\n%d\n" % n)
            f.write("ITEM: NUMBER OF ATOMS\n%d\n" % (len(eles)))
            f.write("ITEM: BOX BOUNDS xy xz yz xx yy zz\n")
            f.write(
                "%f %f %f\n%f %f %f\n %f %f %f\n"
                % (
                    box_bounds[0][0],
                    box_bounds[0][1],
                    box_bounds[0][2],
                    box_bounds[1][0],
                    box_bounds[1][1],
                    box_bounds[1][2],
                    box_bounds[2][0],
                    box_bounds[2][1],
                    box_bounds[2][2],
                )
            )
            f.write("ITEM: ATOMS type x y z id\n")
            for i in range(len(eles)):
                f.write(
                    "%s %f %f %f %d\n"
                    % (
                        eles[i],
                        poses[i, 0],
                        poses[i, 1],
                        poses[i, 2],
                        i + 1,
                    )
                )
    print(f"==> {absdump}")


def write_VESTA(
    in_filename: str,
    data_type,
    out_filename="DS-PAW.cube",
    subtype=None,
    format="cube",
):
    """从包含电子体系信息的json或h5文件中读取数据并写入VESTA格式的文件中

    Parameters
    ----------
    in_filename : str
        包含电子体系信息的json或h5文件路径
    data_type: str
        数据类型，支持 "rho", "potential", "elf", "pcharge", "rhoBound"
    out_filename : str
        输出文件路径, 默认 "DS-PAW.cube"
    subtype : str
        用于指定data_type的数据子类型，默认为None，将读取 potential 的 TotalElectrostaticPotential 数据
    format : str
        输出的数据格式，支持 "cube" 和 "vesta" （"vasp"），默认为 "cube"，大小写不敏感

    Returns
    --------
    out_filename : file
        VESTA格式的文件

    Examples
    --------
    >>> from dspawpy.io.write import write_VESTA
    >>> write_VESTA("/data/home/hzw1002/dspawpy_repo/test/2.2/rho.json", "rho", out_filename='/data/home/hzw1002/dspawpy_repo/test/out/rho.cube')
    Reading /data/home/hzw1002/dspawpy_repo/test/2.2/rho.json...
    ==> /data/home/hzw1002/dspawpy_repo/test/out/rho.cube
    """
    if in_filename.endswith(".h5"):
        data = load_h5(in_filename)
        structure = build_Structures_from_datafile(in_filename)[0]
        grid = data["/AtomInfo/Grid"]  # get grid array
        if data_type == "rho" or data_type == "rhoBound":
            vd = data["/Rho/TotalCharge"]
        elif data_type == "potential":
            if subtype is None:
                subtype = "TotalElectrostaticPotential"
            vd = data[f"/Potential/{subtype}"]
        elif data_type == "elf":
            vd = data["/ELF/TotalELF"]
        elif data_type == "pcharge":
            vd = data["/Pcharge/1/TotalCharge"]
        else:
            raise NotImplementedError("Only support rho/potential/elf/pcharge/rhoBound")

    elif in_filename.endswith(".json"):
        with open(in_filename, "r") as fin:
            data = json.load(fin)
        structure = build_Structures_from_datafile(in_filename)[0]
        grid = data["AtomInfo"]["Grid"]  # get grid array
        if data_type == "rho" or data_type == "rhoBound":
            vd = data["Rho"]["TotalCharge"]
        elif data_type == "potential":
            if subtype is None:
                subtype = "TotalElectrostaticPotential"
            vd = data["Potential"][subtype]
        elif data_type == "elf":
            vd = data["ELF"]["TotalELF"]
        elif data_type == "pcharge":
            vd = data["Pcharge"][0]["TotalCharge"]
        else:
            raise NotImplementedError("Only support rho/potential/elf/pcharge/rhoBound")

    else:
        raise NotImplementedError("Only support json/h5 format")

    _write_specific_format(structure, grid, vd, out_filename, format=format)


def write_delta_rho_vesta(total, individuals, output="delta_rho.cube", format="cube"):
    """电荷密度差分可视化

    DeviceStudio暂不支持大文件，临时写成可以用VESTA打开的格式

    Parameters
    ----------
    total : str
        体系总电荷密度文件路径，可以是h5或json格式
    individuals : list of str
        体系各组分电荷密度文件路径，可以是h5或json格式
    output : str
        输出文件路径，默认 "delta_rho.cube"
    format : str
        输出的数据格式，支持 "cube" 和 "vasp"，默认为 "cube"

    Returns
    -------
    output : file
        电荷差分（total-individual1-individual2-...）后的电荷密度文件，

    Examples
    --------
    >>> from dspawpy.io.write import write_delta_rho_vesta
    >>> write_delta_rho_vesta(total='/data/home/hzw1002/dspawpy_repo/test/supplement/AB.h5',
    ...     individuals=['/data/home/hzw1002/dspawpy_repo/test/supplement/A.h5', '/data/home/hzw1002/dspawpy_repo/test/supplement/B.h5'],
    ...     output='/data/home/hzw1002/dspawpy_repo/test/out/delta_rho.cube')
    Reading /data/home/hzw1002/dspawpy_repo/test/supplement/AB.h5...
    Reading /data/home/hzw1002/dspawpy_repo/test/supplement/A.h5...
    Reading /data/home/hzw1002/dspawpy_repo/test/supplement/B.h5...
    ==> /data/home/hzw1002/dspawpy_repo/test/out/delta_rho.cube
    """
    abstotal = os.path.abspath(total)
    structure = build_Structures_from_datafile(abstotal)[0]
    if abstotal.endswith(".h5"):
        dataAB = load_h5(abstotal)
        rho = np.array(dataAB["/Rho/TotalCharge"])
        grid = dataAB["/AtomInfo/Grid"]
    elif abstotal.endswith(".json"):
        with open(abstotal, "r") as f1:
            dataAB = json.load(f1)
            rho = np.array(dataAB["Rho"]["TotalCharge"])
            grid = dataAB["AtomInfo"]["Grid"]

    else:
        raise ValueError(f"file format must be either h5 or json: {abstotal}")

    for individual in individuals:
        absindividual = os.path.abspath(individual)
        print(f"Reading {individual}...")
        if absindividual.endswith(".h5"):
            data_individual = load_h5(absindividual)
            rho_individual = np.array(data_individual["/Rho/TotalCharge"])
        elif absindividual.endswith(".json"):
            with open(absindividual, "r") as f2:
                data_individual = json.load(f2)
                rho_individual = np.array(data_individual["Rho"]["TotalCharge"])
        else:
            raise ValueError(f"file format must be either h5 or json: {absindividual}")

        rho -= rho_individual

    volumetricData = np.array(rho)
    _write_specific_format(
        structure, grid, volumetricData, filename=output, format=format
    )


def to_file(structure, filename: str, fmt=None, coords_are_cartesian=True, si=None):
    r"""往结构文件中写入信息

    Parameters
    ----------
    structure : Structure
        pymatgen的Structure对象
    filename : str
        结构文件名
    fmt : str
        - 结构文件类型，原生支持 'json', 'as', 'hzw', 'pdb', 'xyz', 'dump' 六种
    coords_are_cartesian : bool
        - 是否写作笛卡尔坐标，默认为True；否则写成分数坐标形式
        - 此选项暂时仅对 as 和 json 格式有效
    si : int
        结构编号索引

    Examples
    --------

    先读取结构信息:

    >>> from dspawpy.io.structure import build_Structures_from_datafile
    >>> s = build_Structures_from_datafile('/data/home/hzw1002/dspawpy_repo/test/2.15/01/neb01.h5')
    Reading /data/home/hzw1002/dspawpy_repo/test/2.15/01/neb01.h5...
    >>> len(s)
    17

    将结构信息写入文件：

    >>> from dspawpy.io.write import to_file
    >>> to_file(s, filename='/data/home/hzw1002/dspawpy_repo/test/out/PtH.json', coords_are_cartesian=True)
    ==> /data/home/hzw1002/dspawpy_repo/test/out/PtH.json
    >>> to_file(s, filename='/data/home/hzw1002/dspawpy_repo/test/out/PtH.as', coords_are_cartesian=True)
    ==> /data/home/hzw1002/dspawpy_repo/test/out/PtH.as
    >>> to_file(s, filename='/data/home/hzw1002/dspawpy_repo/test/out/PtH.hzw', coords_are_cartesian=True)
    ==> /data/home/hzw1002/dspawpy_repo/test/out/PtH.hzw

    pdb, xyz, dump 三种类型的文件，可以写入多个构型，形成“轨迹”。生成的 xyz 等轨迹文件可使用 OVITO 等可视化软件打开观察。

    >>> to_file(s, filename='/data/home/hzw1002/dspawpy_repo/test/out/PtH.pdb', coords_are_cartesian=True)
    ==> /data/home/hzw1002/dspawpy_repo/test/out/PtH.pdb
    >>> to_file(s, filename='/data/home/hzw1002/dspawpy_repo/test/out/PtH.xyz', coords_are_cartesian=True)
    ==> /data/home/hzw1002/dspawpy_repo/test/out/PtH.xyz
    >>> to_file(s, filename='/data/home/hzw1002/dspawpy_repo/test/out/PtH.dump', coords_are_cartesian=True)
    ==> /data/home/hzw1002/dspawpy_repo/test/out/PtH.dump

    单结构信息推荐使用 as 格式存储，如果 Structure 中有磁矩或自由度信息，将会按最完整的格式统一写入，形如 Fix_x, Fix_y, Fix_z, Mag_x, Mag_y, Mag_z，自由度信息默认为 F，磁矩默认为 0.0。可视情况自行手动删除生成的 as 文件中的这些默认信息

    >>> with open('/data/home/hzw1002/dspawpy_repo/test/out/PtH.as') as f:
    ...     print(f.read())
    ...
    Total number of atoms
    13
    Lattice Fix_x Fix_y Fix_z
     5.60580000 0.00000000 0.00000000 F F F
     0.00000000 5.60580000 0.00000000 F F F
     0.00000000 0.00000000 16.81740000 F F F
    Cartesian Fix_x Fix_y Fix_z Mag
    H 2.58985263 3.72755271 6.94246998 F F F 0.0
    Pt 1.37942121 1.39655502 1.96304099 F F F 0.0
    Pt 4.20055071 1.40326436 1.94681875 F F F 0.0
    Pt 1.37462277 4.20932677 2.00221003 F F F 0.0
    Pt 4.21197615 4.21324064 1.99578112 F F F 0.0
    Pt 5.58740047 5.59517338 3.93274445 F F F 0.0
    Pt 5.58633749 2.78068345 3.91301343 F F F 0.0
    Pt 2.79076605 5.59305895 3.91208092 F F F 0.0
    Pt 2.78904685 2.78501463 3.89610696 F F F 0.0
    Pt 1.38102265 1.36691874 5.84326681 F F F 0.0
    Pt 4.19057728 1.36788897 5.84877666 F F F 0.0
    Pt 1.34667410 4.16198043 5.89298591 F F F 0.0
    Pt 4.17046728 4.15729941 5.89874209 F F F 0.0
    <BLANKLINE>

    写成其他类型的结构文件，将忽略磁矩和自由度信息
    """
    if si is not None:
        assert isinstance(si, int), "si should be an integer used to index the list"
    if isinstance(structure, Structure):
        structure = [structure]

    absfilename = os.path.abspath(filename)
    if fmt is None:
        fmt = absfilename.split(".")[-1]

    if fmt == "pdb":  # 可以是多个构型
        if si:
            _to_pdb(structure[si], absfilename)
        else:
            _to_pdb(structure, absfilename)
    elif fmt == "xyz":  # 可以是多个构型
        if si:
            _write_xyz_traj(structure[si], absfilename)
        else:
            _write_xyz_traj(structure, absfilename)
    elif fmt == "dump":  # 可以是多个构型
        if si:
            _write_dump_traj(structure[si], absfilename)
        else:
            _write_dump_traj(structure, absfilename)

    elif fmt == "json":  # 单个构型
        if si:
            _to_dspaw_json(structure[si], absfilename, coords_are_cartesian)
        else:
            _to_dspaw_json(structure[-1], absfilename, coords_are_cartesian)
    elif fmt == "as":
        if si:
            _to_dspaw_as(structure[si], absfilename, coords_are_cartesian)
        else:
            _to_dspaw_as(structure[-1], absfilename, coords_are_cartesian)
    elif fmt == "hzw":
        if si:
            _to_hzw(structure[si], absfilename)
        else:
            _to_hzw(structure[-1], absfilename)

    elif fmt in [
        "cif",
        "mcif",
        "poscar",
        "cssr",
        "xsf",
        "mcsqs",
        "yaml",
        "fleur-inpgen",
        "prismatic",
        "res",
    ]:
        if si:
            structure[si].to(filename=absfilename, fmt=fmt)
        else:
            structure[-1].to(filename=absfilename, fmt=fmt)

    else:
        try:
            if si:
                structure[si].to(filename=absfilename)
            else:
                structure[-1].to(filename=absfilename)
        except Exception as e:
            raise NotImplementedError(
                f"formats other that [pdb, xyz, dump, json, as, hzw] are handled by pymatgen, while it returns: {e}"
            )


def _write_atoms(fileobj, structure, idirect=False):
    fileobj.write("DS-PAW Structure\n")
    fileobj.write("  1.00\n")
    lattice = structure.lattice.matrix.reshape(-1, 1)
    fileobj.write("%g %g %g\n" % (lattice[0][0], lattice[1][0], lattice[2][0]))
    fileobj.write("%g %g %g\n" % (lattice[3][0], lattice[4][0], lattice[5][0]))
    fileobj.write("%g %g %g\n" % (lattice[6][0], lattice[7][0], lattice[8][0]))

    elements = [s.species_string for s in structure.sites]
    elements_set = []
    elements_number = {}
    for e in elements:
        if e in elements_set:
            elements_number[e] = elements_number[e] + 1
        else:
            elements_set.append(e)
            elements_number[e] = 1

    for e in elements_set:
        fileobj.write("  " + e)
    fileobj.write("\n")

    for e in elements_set:
        fileobj.write("%g " % (elements_number[e]))
    fileobj.write("\n")
    if idirect:
        fileobj.write("Direct\n")
        for i, p in enumerate(structure.frac_coords):
            fileobj.write("%g %g %g\n" % (p[0], p[1], p[2]))
    else:
        fileobj.write("Cartesian\n")
        for i, p in enumerate(structure.cart_coords):
            fileobj.write("%g %g %g\n" % (p[0], p[1], p[2]))


def _write_specific_format(structure, grid, volumetricData, filename, format="cube"):
    """Write to file with specific volumetric data format.
    structure: Structure
        Pymatgen Structure specifying the atomic configuration.
    grid : 3dim numpy array
        such as 180 x 180 x 180
    volumetricData : numpy array
        Array containing volumetric data as e.g. electronic density
    filename : str
        Name of the file to write to.
    format : str
        Format of the file to write to. Default to cube, can be vesta
    """
    absfile = os.path.abspath(filename)
    if os.path.isfile(absfile):
        print("Warning: %s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)

    # normalize volumetric data
    vd = np.asarray(volumetricData)
    vd /= np.sum(vd)

    if format.lower() == "cube":
        with open(absfile, "w") as fileobj:
            # 1+2 注释
            fileobj.write("Cube file written on " + time.strftime("%c"))
            fileobj.write("\nOUTER LOOP: X, MIDDLE LOOP: Y, INNER LOOP: Z\n")
            # 3 原子总数+原点坐标
            origin = np.zeros(3)
            fileobj.write(
                f"{len(structure.sites)} {origin[0]} {origin[1]} {origin[2]}\n"
            )
            # 4+5+6 格点数+voxel矢量
            for i in range(3):
                # 单位为波尔
                n = grid[i]
                d = structure.lattice.matrix[i] / n / Bohr
                fileobj.write(f"{n} {d[0]} {d[1]} {d[2]}\n")

            # 7,8,... 原子序数+原子坐标
            positions = structure.cart_coords / Bohr
            species_string = [s.species_string for s in structure.sites]
            # remove + and - from species_string
            species_string = [
                s.replace("+", "").replace("-", "") for s in species_string
            ]
            symbols = "".join(species_string)  # SiH
            numbers = _symbols2numbers(symbols)
            for Z, (x, y, z) in zip(numbers, positions):
                fileobj.write(f"{Z} {0.0} {x} {y} {z}\n")

            # 由于cube格式的特殊规定，数组需要按格点数反向reshape后再转置才对
            # 后面那个浮点数用于单位转换，尚不清楚物理意义
            reshaped_vd = (
                vd.reshape(grid[::-1]).T * 0.0035626635627220541406318925434652
            )

            if reshaped_vd.dtype == complex:
                reshaped_vd = np.abs(reshaped_vd)
            reshaped_vd.tofile(fileobj, sep="\n", format="%e")

    elif format.lower() == "vesta" or format.lower() == "vasp":
        with open(absfile, "w") as file:
            _write_atoms(file, structure, idirect=True)  # 默认直角坐标
            file.write(f"{grid[0]} {grid[1]} {grid[2]}\n")
            i = 0
            while i < len(vd):
                for j in range(10):  # 比一行只写一个似乎能让文件更小
                    file.write(f"{vd[i]} ")
                    i += 1
                    if i >= len(vd):
                        break
            file.write("\n")

    else:
        raise NotImplementedError(' only "cube" and "vesta" are supported.')

    print(f"==> {absfile}")


def _to_dspaw_as(structure, filename: str, coords_are_cartesian=True):
    """write dspaw structure file of .as type"""
    absfile = os.path.abspath(filename)
    if os.path.isfile(absfile):
        warnings.warn("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        file.write("Total number of atoms\n")
        file.write("%d\n" % len(structure))

        # ^ write lattice info
        if "LatticeFixs" in structure.sites[0].properties:
            lfinfo = structure.sites[0].properties["LatticeFixs"]
            if len(lfinfo) == 3:
                file.write("Lattice Fix\n")
                formatted_fts = []
                for ft in lfinfo:
                    if ft == "True":  # True
                        ft_formatted = "T"
                    else:
                        ft_formatted = "F"
                    formatted_fts.append(ft_formatted)
                for v in structure.lattice.matrix:
                    # write each element of formatted_fts in a line without [] symbol
                    file.write(f'{v} {formatted_fts}.strip("[").strip("]")\n')
            elif len(lfinfo) == 9:
                file.write("Lattice Fix_x Fix_y Fix_z\n")
                formatted_fts = []
                for ft in lfinfo:
                    if ft == "True":  # True
                        ft_formatted = "T"
                    else:
                        ft_formatted = "F"
                    formatted_fts.append(ft_formatted)
                fix_str1 = " ".join(formatted_fts[:3])
                fix_str2 = " ".join(formatted_fts[3:6])
                fix_str3 = " ".join(formatted_fts[6:9])
                v1 = structure.lattice.matrix[0]
                v2 = structure.lattice.matrix[1]
                v3 = structure.lattice.matrix[2]
                file.write(f" {v1[0]:5.8f} {v1[1]:5.8f} {v1[2]:5.8f} {fix_str1}\n")
                file.write(f" {v2[0]:5.8f} {v2[1]:5.8f} {v2[2]:5.8f} {fix_str2}\n")
                file.write(f" {v3[0]:5.8f} {v3[1]:5.8f} {v3[2]:5.8f} {fix_str3}\n")
            else:
                raise ValueError(
                    f"LatticeFixs should be a list of 3 or 9 bools, but got {lfinfo}"
                )
        else:
            file.write("Lattice\n")
            for v in structure.lattice.matrix:
                file.write("%.8f %.8f %.8f\n" % (v[0], v[1], v[2]))

        i = 0
        for site in structure:
            keys = []
            for key in site.properties:  # site.properties is a dictionary
                if key != "LatticeFixs":
                    keys.append(key)
            keys.sort()
            keys_str = " ".join(keys)  # sth like 'magmom fix
            if i == 0:
                if coords_are_cartesian:
                    file.write(f"Cartesian {keys_str}\n")
                else:
                    file.write(f"Direct {keys_str}\n")
            i += 1

            coords = site.coords if coords_are_cartesian else site.frac_coords
            raw = []
            for sortted_key in keys:  # site.properties is a dictionary
                raw_values = site.properties[sortted_key]
                if isinstance(raw_values, list):  # single True or False
                    values = raw_values
                else:
                    values = [raw_values]
                for v in values:
                    if v == "True":
                        value_str = "T"
                    elif v == "False":
                        value_str = "F"
                    else:
                        value_str = str(v)
                    raw.append(value_str)

            final_strs = " ".join(raw)  # sth like '0.0 T
            file.write(
                "%s %.8f %.8f %.8f %s\n"
                % (site.species_string, coords[0], coords[1], coords[2], final_strs)
            )
    print(f"==> {absfile}")


def _to_hzw(structure, filename: str):
    """write hzw structure file of .hzw type"""
    absfile = os.path.abspath(filename)

    if os.path.isfile(absfile):
        warnings.warn("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        file.write("% The number of probes \n")
        file.write("0\n")
        file.write("% Uni-cell vector\n")

        for v in structure.lattice.matrix:
            file.write("%.6f %.6f %.6f\n" % (v[0], v[1], v[2]))

        file.write("% Total number of device_structure\n")
        file.write("%d\n" % len(structure))
        file.write("% Atom site\n")

        for site in structure:
            file.write(
                "%s %.6f %.6f %.6f\n"
                % (site.species_string, site.coords[0], site.coords[1], site.coords[2])
            )
    print(f"==> {absfile}")


def _to_dspaw_json(structure, filename: str, coords_are_cartesian=True):
    """write dspaw structure file of .json type"""
    absfile = os.path.abspath(filename)
    lattice = structure.lattice.matrix.flatten().tolist()
    atoms = []
    for site in structure:
        coords = site.coords if coords_are_cartesian else site.frac_coords
        atoms.append({"Element": site.species_string, "Position": coords.tolist()})

    coordinate_type = "Cartesian" if coords_are_cartesian else "Direct"
    d = {"Lattice": lattice, "CoordinateType": coordinate_type, "Atoms": atoms}
    if os.path.isfile(absfile):
        warnings.warn("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        json.dump(d, file, indent=4)
    print(f"==> {absfile}")


def _to_pdb(structures, filename: str):
    """write pdb structure file of .pdb type"""
    absfile = os.path.abspath(filename)
    if not isinstance(structures, list):
        structures = [structures]
    if os.path.isfile(absfile):
        warnings.warn("%s already exists and will be overwritten!" % absfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    with open(absfile, "w", encoding="utf-8") as file:
        for i, s in enumerate(structures):
            file.write("MODEL         %d\n" % (i + 1))
            file.write("REMARK   Converted from Structures\n")
            file.write("REMARK   Converted using dspawpy\n")
            lengths = s.lattice.lengths
            angles = s.lattice.angles
            file.write(
                "CRYST1{0:9.3f}{1:9.3f}{2:9.3f}{3:7.2f}{4:7.2f}{5:7.2f}\n".format(
                    lengths[0], lengths[1], lengths[2], angles[0], angles[1], angles[2]
                )
            )
            for j, site in enumerate(s):
                file.write(
                    "%4s%7d%4s%5s%6d%4s%8.3f%8.3f%8.3f%6.2f%6.2f%12s\n"
                    % (
                        "ATOM",
                        j + 1,
                        site.species_string,
                        "MOL",
                        1,
                        "    ",
                        site.coords[0],
                        site.coords[1],
                        site.coords[2],
                        1.0,
                        0.0,
                        site.species_string,
                    )
                )
            file.write("TER\n")
            file.write("ENDMDL\n")

    print(f"==> {absfile}")

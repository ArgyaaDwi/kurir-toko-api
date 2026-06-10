BRANCHES_DEFAULT = [
    {"kode": "SUB", "nama": "Surabaya", "lat": -7.317566, "lng": 112.764234},
    {"kode": "JKT", "nama": "Jakarta", "lat": -6.208800, "lng": 106.845600},
    {"kode": "MLG", "nama": "Malang", "lat": -7.979700, "lng": 112.630400},
    {"kode": "SMG", "nama": "Semarang", "lat": -6.966700, "lng": 110.416700},
    {"kode": "JOG", "nama": "Yogyakarta", "lat": -7.795600, "lng": 110.369500},
    {"kode": "BLI", "nama": "Bali", "lat": -8.340500, "lng": 115.092000},
]


def get_branch_by_code(branch_code: str) -> dict:
    for branch in BRANCHES_DEFAULT:
        if branch["kode"] == branch_code:
            return branch
    raise ValueError(f"Unknown branch code: {branch_code}")


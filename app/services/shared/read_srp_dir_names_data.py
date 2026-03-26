from django.conf import settings

def read_srp_dir_names_data():
    srp_infos = settings.SRP_INFO

    sra_studies = []
    for srp_info in srp_infos:
        sra_studies.append(srp_info['SRAStudy'])
    duplicate_sra_studies = list(set(sra_studies))

    result = {
        'data': duplicate_sra_studies
    }

    return result



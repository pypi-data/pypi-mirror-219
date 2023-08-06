def dq_searching_rules(category_rule=None, table_name=None, rule_id=None, static_id=None, sequence="001"):
    from spark_generated_rules_tools.utils import BASE_DIR
    from spark_generated_rules_tools import get_color, get_color_b
    import os
    import json
    import ast
    import sys

    is_windows = sys.platform.startswith('win')
    json_resource_rules = os.path.join(BASE_DIR, "utils", "resource", "rules.json")

    if is_windows:
        json_resource_rules = json_resource_rules.replace("\\", "/")

    with open(json_resource_rules) as f:
        default_rules = json.load(f)
    rules_config = default_rules.get("rules_config", None)
    hamu_dict = dict()
    id_key_dict = dict()
    rs_dict = dict()
    for k, v in rules_config.items():
        for key_name, value_name in v.items():
            rules_version = value_name[0].get("rules_version")
            rules_class = str(value_name[0].get("rules_class"))
            rules_columns = value_name[0].get("rules_columns")
            rules_description = value_name[0].get("rules_name")
            if rules_version == rule_id:
                print(f"{get_color(rules_version)} => {get_color_b(rules_description)}")
                for rule_name, rule_dtype in rules_columns[0].items():
                    if rule_dtype[1] == "True":
                        id_key_dict[rule_name] = "Mandatory"
                    if rule_dtype[0] == "Boolean" and rule_dtype[2] == "True":
                        rules_value = True
                    elif rule_dtype[0] == "Boolean" and rule_dtype[2] == "False":
                        rules_value = False
                    elif rule_dtype[0] == "Double" and rule_dtype[2] == "100":
                        rules_value = ast.literal_eval(rule_dtype[2])
                    elif rule_dtype[0] == "String" and rule_dtype[2] in ("None", ""):
                        rules_value = ""
                    elif rule_dtype[0] == "Array[String]" and rule_dtype[2] in ("None", ""):
                        rules_value = ["default"]
                    elif rule_dtype[0] == "Dict" and rule_dtype[2] in ("None", ""):
                        rules_value = dict(type="", paths="")
                    else:
                        rules_value = rule_dtype[2]
                    rs_dict[rule_name] = rules_value
                if static_id:
                    rs_dict["id"] = static_id
                else:
                    rule_id = str(rule_id).replace("-1", "").replace("-2", "").strip()
                    rs_dict["id"] = f"PE_{category_rule}_{table_name}_{rule_id}_{sequence}"
                hamu_dict["class"] = rules_class
                hamu_dict["config"] = rs_dict
    return hamu_dict, id_key_dict


def dq_convert_url_bitbucket_artifactory(url_conf=None):
    url = url_conf
    url_conf_name = str(str(url).split("/")[-3])
    url_conf_name = f"{url_conf_name}"
    url_conf_zone = str(str(url).split("/")[-2])
    uuaa_name = str(str(url).split("/")[-4])
    url_conf = f"http://artifactory-gdt.central-02.nextgen.igrupobbva/" \
               f"artifactory/gl-datio-generic-local/" \
               f"kirby/" \
               f"pe/" \
               f"{uuaa_name.lower()}/" \
               f"{url_conf_zone.lower()}/" \
               f"{url_conf_name.lower()}/" \
               f"0.1.0/" \
               f"{url_conf_name.lower()}.conf"
    return url_conf


def dq_creating_directory_sandbox(path=None):
    from spark_generated_rules_tools import get_color, get_color_b
    import os

    if path in ("", None):
        raise Exception(f'required variable path')
    if not os.path.exists(f'{path}'):
        os.makedirs(f'{path}')
        print(f"{get_color('Directory Created:')} {get_color_b(path)}")
    else:
        print(f"{get_color('Directory Exists:')} {get_color_b(path)}")


def dq_path_workspace(user_sandbox=None):
    import os
    import sys

    if user_sandbox is None:
        user_sandbox = os.getenv('JPY_USER')
        print(f"user_sandbox = {user_sandbox}")
        if user_sandbox in ("", None):
            raise Exception(f'required variable user_sandbox')
    is_windows = sys.platform.startswith('win')
    pj_dir_workspace = ""

    pj_dq_dir_name = "data_quality_rules"
    pj_dq_dir_name = os.path.join(pj_dir_workspace, pj_dq_dir_name)
    pj_dq_dir_confs_name = os.path.join(pj_dir_workspace, pj_dq_dir_name, "data_confs")
    pj_dq_dir_hocons_name = os.path.join(pj_dir_workspace, pj_dq_dir_name, "data_hocons")
    pj_dq_dir_mvp_name = os.path.join(pj_dir_workspace, pj_dq_dir_name, "data_mvp")

    if is_windows:
        pj_dq_dir_name = pj_dq_dir_name.replace("\\", "/")
        pj_dq_dir_confs_name = pj_dq_dir_confs_name.replace("\\", "/")
        pj_dq_dir_hocons_name = pj_dq_dir_hocons_name.replace("\\", "/")
        pj_dq_dir_mvp_name = pj_dq_dir_mvp_name.replace("\\", "/")

    dq_creating_directory_sandbox(path=pj_dq_dir_name)
    dq_creating_directory_sandbox(path=pj_dq_dir_confs_name)
    dq_creating_directory_sandbox(path=pj_dq_dir_hocons_name)
    dq_creating_directory_sandbox(path=pj_dq_dir_mvp_name)
    os.environ['pj_dq_dir_name'] = pj_dq_dir_name
    os.environ['pj_dq_dir_confs_name'] = pj_dq_dir_confs_name
    os.environ['pj_dq_dir_hocons_name'] = pj_dq_dir_hocons_name
    os.environ['pj_dq_dir_mvp_name'] = pj_dq_dir_mvp_name
    os.environ['pj_dir_workspace'] = pj_dir_workspace


def dq_get_rules_list():
    import os
    import json
    import sys
    from prettytable import PrettyTable
    from spark_generated_rules_tools.utils.color import get_color_b
    from spark_generated_rules_tools.utils import BASE_DIR

    is_windows = sys.platform.startswith('win')
    json_resource_rules = os.path.join(BASE_DIR, "utils", "resource", "rules.json")

    if is_windows:
        json_resource_rules = json_resource_rules.replace("\\", "/")

    with open(json_resource_rules) as f:
        default_rules = json.load(f)
    rules_config = default_rules.get("rules_config", None)

    t = PrettyTable()
    t.field_names = [get_color_b("DQ NAME"), get_color_b("VERSION")]
    for k, v in rules_config.items():
        for key_name, value_name in v.items():
            t.add_row([key_name, value_name[0].get("rules_version")])
    print(t)


def dq_generated_rules(rule_id=None,
                       table_name=None,
                       category_rule="MVP"):
    import os
    import sys
    import json
    from pyhocon import ConfigFactory
    from pyhocon.converter import HOCONConverter
    from spark_generated_rules_tools.utils.color import get_color_b, get_color
    from prettytable import PrettyTable

    is_windows = sys.platform.startswith('win')
    dir_hocons_name = os.getenv('pj_dq_dir_hocons_name')
    uuaa_name = str(table_name.split("_")[1]).upper()
    dir_hocons_filename = os.path.join(dir_hocons_name, uuaa_name, f"{table_name}_{rule_id}_generated.conf")

    if is_windows:
        dir_hocons_filename = dir_hocons_filename.replace("\\", "/")
    os.makedirs(os.path.dirname(dir_hocons_filename), exist_ok=True)

    rs_list = list()
    hamu_dict, id_key_dict = dq_searching_rules(category_rule=category_rule, table_name=table_name,
                                                rule_id=rule_id, static_id=None, sequence="001")
    rs_list.append(hamu_dict)
    json_file2 = json.dumps(rs_list, indent=4)
    conf2 = ConfigFactory.parse_string(json_file2)
    hocons_file2 = HOCONConverter.convert(conf2, "hocon")
    with open(dir_hocons_filename, "w") as f:
        f.write(hocons_file2)

    print(f"{get_color(f'========CREATE RULE============')} ")
    with open(dir_hocons_filename) as f:
        res = f.read()
    print(f"{get_color_b(f'{res}')}")

    print(f"{get_color(f'========MANDATORY============')} ")
    t = PrettyTable()
    t.field_names = [get_color_b("DQ NAME"), get_color_b("TYPE")]
    for key_name, value_name in id_key_dict.items():
        t.add_row([key_name, value_name])
    print(t)

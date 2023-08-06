def flatten(json_data):
    updated_json_list = []

    if type(json_data) == list:
        for json_object in json_data:
            to_be_flat_dict = {}

            for d_k, d_v in json_object.items():
                if type(d_v) == dict:
                    to_be_flat_dict.update(dict_flatten_json(d_k, d_v))

                elif type(d_v) == list:
                    to_be_flat_dict.update(list_flatten_json(d_k, d_v))

                else:
                    to_be_flat_dict[d_k] = d_v

            updated_json_list.append(to_be_flat_dict)

    elif type(json_data) == dict:
        to_be_flat_dict = {}
        for d_k, d_v in json_data.items():
            if type(d_v) == dict:
                data = dict_flatten_json(d_k, d_v)
                to_be_flat_dict.update(data)

            elif type(d_v) == list:
                to_be_flat_dict.update(list_flatten_json(d_k, d_v))

            else:
                to_be_flat_dict[d_k] = d_v

        updated_json_list.append(to_be_flat_dict)

    else:
        pass

    return updated_json_list


def dict_flatten_json(dict_key, dict_value, c_str=None):
    dictionary_fun_dict = {}

    for d_k, d_v in dict_value.items():
        if type(d_v) == dict:
            if c_str:
                dictionary_fun_dict.update(
                    dict_flatten_json(d_k, d_v, c_str=str(c_str) + str(dict_key))
                )
            else:
                dictionary_fun_dict.update(
                    dict_flatten_json(d_k, d_v, c_str=str(dict_key))
                )

        if type(d_v) == list:
            if c_str:
                dictionary_fun_dict.update(
                    list_flatten_json(d_k, d_v, c_str=str(c_str) + str(dict_key))
                )
            else:
                dictionary_fun_dict.update(
                    list_flatten_json(d_k, d_v, c_str=str(dict_key))
                )

        else:
            if c_str:
                dictionary_fun_dict[
                    str(c_str) + "_" + str(dict_key) + "_" + str(d_k)
                ] = d_v

            else:
                dictionary_fun_dict[str(dict_key) + "_" + str(d_k)] = d_v

    return dictionary_fun_dict


def list_flatten_json(d_k, d_v, c_str=None):
    list_fun_dict = {}

    for lst_index, lst_obj in enumerate(d_v):
        if type(lst_obj) == dict:
            if c_str:
                list_fun_dict.update(
                    dict_flatten_json(lst_index, lst_obj, c_str=c_str + d_k)
                )
            else:
                list_fun_dict.update(
                    dict_flatten_json(lst_index, lst_obj, c_str=str(d_k))
                )

        elif type(lst_obj) == list:
            if c_str:
                list_fun_dict.update(
                    list_flatten_json(d_k, d_v, c_str=str(c_str) + str(d_k))
                )
            else:
                list_fun_dict.update(list_flatten_json(d_k, d_v, c_str=str(d_k)))

        else:
            if c_str:
                list_fun_dict[
                    str(c_str) + "_" + str(d_k) + "_" + str(lst_index)
                ] = lst_obj
            else:
                list_fun_dict[str(d_k) + "_" + str(lst_index)] = lst_obj

    return list_fun_dict

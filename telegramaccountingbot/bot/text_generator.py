

def balance_dict_to_message(dict_id_to_name, balance_dict):
    average = balance_dict["average"]
    message = "average paid: %.2f\n" % average
    message += "=" * (len(message.split("\n")[-2]))
    message += "\n"
    for _id in balance_dict.keys():
        if _id == "average":
            continue
        message += _get_balance_line(dict_id_to_name[_id],
                                     balance_dict[_id],
                                     average)
        message += "\n"
    return message


def _get_balance_line(name, value, average):
    diff = value - average
    if diff < 0:
        sign = "-"
    else:
        sign = "+"        
    line = "%s: %.2f (%s%.2f)" % (name, value, sign, diff)
    return line
    

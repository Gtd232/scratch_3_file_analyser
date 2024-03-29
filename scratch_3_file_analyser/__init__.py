# -*- coding: utf-8 -*
r"""
灵感来源于https://aerfaying.com/Projects/512945
同时借鉴了它
analyze函数需要传入一个参数，是json文件，但要转换成字符串。可以将sb3文件转换成analyze参数输入的字符串的函数式unzip。详见DEMO.py
若无DEMO.py，见以下代码：
import scratch_3_file_analyser
print(scratch_3_file_analyser.analyze(scratch_3_file_analyser.unzip('./DEMO.sb3')))
"""

author = ['Gtd232']
__version__ = '1.0.0'


def unzip(path: str):
    r"""
    该函数可输入一个.sb3文件（路径），然后可提取project.json并输出字符串。
    :param path:
    :return:
    """
    from os.path import isfile
    from zipfile import ZipFile

    if isfile(path):
        return open(ZipFile(path, 'r').extract('project.json'), 'r').read()
    else:
        raise Exception('这不是一个目录。')


def analyze(file: str):
    r"""
    该函数可分析传入的json字符串，并输出一个列表。
    列表每项分别是：
    角色数（含舞台），角色名（含舞台），变量名，列表名，造型总数，音频文件总数，代码块总数，有用的代码块总数（暂不提供），运动类代码块总数，外观类代码块总数，声音类代码块总数，事件类代码块总数，控制类代码块总数，侦测类代码块总数，运算类代码块总数，变量（或列表）操作类代码块总数，其它类代码块总数,帽子型代码块总数，有用的帽子型代码块总数，
    以后会上线扩展类代码块数。
    :param file:
    :return:
    """
    from json import loads
    d = loads(file)
    r = [len(d["targets"])]
    sprite_name = [i["name"] for i in d["targets"]]
    r.append(sprite_name)  # 添加所有精灵的名称

    variable_name = []
    for i in range(len(d["targets"])):  # ["variables"].keys():
        variable_name.extend(
            d["targets"][i]["variables"][i2][0]
            for i2 in d["targets"][i]["variables"].keys()
        )
    r.append(variable_name)

    list_name = []
    for i in range(len(d["targets"])):  # ["variables"].keys():
        list_name.extend(
            d["targets"][i]["lists"][i2][0]
            for i2 in d["targets"][i]["lists"].keys()
        )
    r.append(list_name)

    costumes = 0
    sounds = 0
    for i in range(len(d["targets"])):  # ["variables"].keys():
        costumes += len(d["targets"][i]["costumes"])
        sounds += len(d["targets"][i]["sounds"])
    r.extend((costumes, sounds))
    blocks = 0
    motion_blocks = 0
    looks_blocks = 0
    sound_blocks = 0
    event_blocks = 0
    control_blocks = 0
    sensing_blocks = 0
    data_blocks = 0
    operator_blocks = 0
    procedures_blocks = 0
    other_blocks = 0
    cap_blocks = 0
    useful_cap_blocks = 0
    useful_blocks = 0
    for i in range(len(d["targets"])):
        for i1 in d["targets"][i]["blocks"]:
            try:
                opcode = d["targets"][i]["blocks"][i1]["opcode"]
                if 'menu' not in opcode and 'argument' not in opcode:
                    blocks += 1
                    if 'motion' in opcode:
                        motion_blocks += 1
                    elif 'looks' in opcode:
                        looks_blocks += 1
                    elif 'sound' in opcode:
                        sound_blocks += 1
                    elif 'control' in opcode:
                        control_blocks += 1
                    elif 'sensing' in opcode:
                        sensing_blocks += 1
                    elif 'data' in opcode:
                        data_blocks += 1
                    elif 'operator' in opcode:
                        operator_blocks += 1
                    elif 'event' in opcode:
                        event_blocks += 1
                    elif opcode == 'procedures_call':
                        procedures_blocks += 1
                    elif opcode == 'procedures_definition':
                        procedures_blocks += 1
                        # useful_blocks 由于各种问题，测出来不准，且暂时没有精力，暂时不提供
                        '''
                        useful_blocks += 1
                        '''
                    elif opcode != 'procedures_prototype':
                        other_blocks += 1
                    if 'control_start_as_clone' in opcode or 'when' in opcode:
                        cap_blocks += 1
                        if d["targets"][i]["blocks"][i1]["next"] is not None:
                            useful_cap_blocks += 1
                    # useful_blocks 由于各种问题，测出来不准，且暂时没有精力，暂时不提供
                    '''
                    if 'event' in opcode and 'when' in opcode and not d["targets"][i]["blocks"][i1]["parent"] is None and not 'boardcast' in opcode and bool(d["targets"][i]["blocks"][i1]["next"]) == True:
                        if 'control_start_as_clone' in d["targets"][i]["blocks"][d["targets"][i]["blocks"][i1]["parent"]]["opcode"]:
                            useful_blocks += 1
                    elif not d["targets"][i]["blocks"][i1]["parent"] is None:
                        if 'when' in d["targets"][i]["blocks"][d["targets"][i]["blocks"][i1]["parent"]]["opcode"]:
                            useful_blocks += 1
                    '''
                elif 'argument' in opcode: # TODO:简化代码
                    if (
                        d["targets"][i]["blocks"][
                            d["targets"][i]["blocks"][i1]["parent"]
                        ]["opcode"]
                        is None
                    ):
                        blocks += 1






                    elif d["targets"][i]["blocks"][d["targets"][i]["blocks"][i1]["parent"]]["opcode"] != 'procedures_prototype':
                        blocks += 1
                        # useful_blocks 由于各种问题，测出来不准，且暂时没有精力，暂时不提供
                        '''
                            useful_blocks += 1
                            '''
            except Exception:
                import traceback
                traceback.print_exc()
    r.extend(
        (
            blocks,
            None,
            motion_blocks,
            looks_blocks,
            sound_blocks,
            event_blocks,
            control_blocks,
            sensing_blocks,
            operator_blocks,
            data_blocks,
            procedures_blocks,
            other_blocks,
            cap_blocks,
            useful_cap_blocks,
        )
    )
    return r

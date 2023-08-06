from tkinter import *

from simba.mixins.pop_up_mixin import PopUpMixin
from simba.mixins.config_reader import ConfigReader
from simba.ui.tkinter_functions import DropDownMenu, CreateLabelFrameWithIcon, Entry_Box, LabelFrame, Label
from simba.utils.enums import Keys, Links, Formats
from simba.utils.checks import check_float
from simba.utils.errors import DuplicationError, NoSpecifiedOutputError, InvalidInputError
from simba.data_processors.mutual_exclusivity_corrector import MutualExclusivityCorrector


class MutualExclusivityPupUp(PopUpMixin, ConfigReader):
    def __init__(self,
                 config_path: str):

        ConfigReader.__init__(self, config_path=config_path)
        PopUpMixin.__init__(self, title='MUTUAL EXCLUSIVITY', size=(1000, 400))

        self.rule_cnt_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header='EXCLUSIVITY RULES #', icon_name=Keys.DOCUMENTATION.value, icon_link=Links.PATH_PLOTS.value)
        self.rule_cnt_dropdown = DropDownMenu(self.rule_cnt_frm, '# RULES:', list(range(1, 21)), '25', com=self.create_rules_frames)
        self.rule_cnt_dropdown.setChoices(1)
        self.rule_cnt_frm.grid(row=0, column=0, sticky='NW')
        self.rule_cnt_dropdown.grid(row=0, column=0, sticky='NW')
        self.create_rules_frames(rules_cnt=1)
        self.main_frm.mainloop()

    def create_rules_frames(self, rules_cnt: int):
        if hasattr(self, 'rule_definitions_frame'):
            self.rule_definitions_frame.destroy()
        self.rule_definitions_frame = LabelFrame(self.main_frm, text='RULE DEFINITIONS', font=Formats.LABELFRAME_HEADER_FORMAT.value, pady=5, padx=5)
        self.rule_definitions_frame.grid(row=1, column=0, sticky='NW')
        Label(self.rule_definitions_frame, text='RULE #').grid(row=0, column=0, sticky=NW)
        for cnt, clf_name in enumerate(self.clf_names):
            Label(self.rule_definitions_frame, text=clf_name).grid(row=0, column=cnt+1, sticky=NW)
        Label(self.rule_definitions_frame, text='WINNER').grid(row=0, column=self.clf_cnt + 1, sticky=NW)
        Label(self.rule_definitions_frame, text='THRESHOLD').grid(row=0, column=self.clf_cnt + 2, sticky=NW)
        Label(self.rule_definitions_frame, text='HIGHEST PROBABILITY').grid(row=0, column=self.clf_cnt + 3, sticky=NW)
        Label(self.rule_definitions_frame, text='TIE BREAK').grid(row=0, column=self.clf_cnt + 4, sticky=NW)
        Label(self.rule_definitions_frame, text='SKIP ON EQUAL').grid(row=0, column=self.clf_cnt + 5, sticky=NW)

        self.rules_dict = {}
        for rule_cnt in range(1, rules_cnt+1):
            self.rules_dict[rule_cnt] = {}
            self.rules_dict[rule_cnt]['subordinates'] = {}
            Label(self.rule_definitions_frame, text=str(rule_cnt), font=Formats.LABELFRAME_HEADER_FORMAT.value).grid(row=rule_cnt, column=0, sticky=NW)
            for clf_cnt, clf_name in enumerate(self.clf_names):
                self.rules_dict[rule_cnt]['subordinates'][clf_name] = {}
                self.rules_dict[rule_cnt]['subordinates'][clf_name]['cb_var'] = BooleanVar()
                self.rules_dict[rule_cnt]['subordinates'][clf_name]['cb'] = Checkbutton(self.rule_definitions_frame, variable=self.rules_dict[rule_cnt]['subordinates'][clf_name]['cb_var'])
                self.rules_dict[rule_cnt]['subordinates'][clf_name]['cb'].grid(row=rule_cnt, column=clf_cnt+1, sticky=NW)

        for rule_cnt in range(1, rules_cnt + 1):
            self.rules_dict[rule_cnt]['determinator_dropdown'] = DropDownMenu(self.rule_definitions_frame, '', self.clf_names, '1')
            self.rules_dict[rule_cnt]['determinator_dropdown'].disable()
            self.rules_dict[rule_cnt]['determinator_dropdown'].setChoices(self.clf_names[0])
            self.rules_dict[rule_cnt]['determinator_dropdown'].grid(row=rule_cnt, column=self.clf_cnt+1, sticky=NW)
            self.rules_dict[rule_cnt]['threshold_entry'] = Entry_Box(self.rule_definitions_frame, '', '1')
            self.rules_dict[rule_cnt]['threshold_entry'].entry_set(0.00)
            self.rules_dict[rule_cnt]['threshold_entry'].grid(row=rule_cnt, column=self.clf_cnt + 2, sticky=NW)
            self.rules_dict[rule_cnt]['threshold_entry'].set_state('disable')

        for rule_cnt in range(1, rules_cnt + 1):
            self.rules_dict[rule_cnt]['highest_var'] = BooleanVar(value=True)
            self.rules_dict[rule_cnt]['highest_cb'] = Checkbutton(self.rule_definitions_frame, variable=self.rules_dict[rule_cnt]['highest_var'], command=lambda k=rule_cnt: self.change_threshold_status(k))
            self.rules_dict[rule_cnt]['highest_cb'].grid(row=rule_cnt, column=self.clf_cnt + 3, sticky=NW)

        for rule_cnt in range(1, rules_cnt + 1):
            self.rules_dict[rule_cnt]['winner_dropdown'] = DropDownMenu(self.rule_definitions_frame, '', self.clf_names, '1')
            self.rules_dict[rule_cnt]['winner_dropdown'].setChoices(self.clf_names[0])
            self.rules_dict[rule_cnt]['winner_dropdown'].grid(row=rule_cnt, column=self.clf_cnt + 4, sticky=NW)
        self.create_run_frm(run_function=self.run)

        for rule_cnt in range(1, rules_cnt + 1):
            self.rules_dict[rule_cnt]['skip_on_equal_var'] = BooleanVar(value=False)
            self.rules_dict[rule_cnt]['skip_on_equal_cb'] = Checkbutton(self.rule_definitions_frame, variable=self.rules_dict[rule_cnt]['skip_on_equal_var'], command=lambda k=rule_cnt: self.change_winner_status(k))
            self.rules_dict[rule_cnt]['skip_on_equal_cb'].grid(row=rule_cnt, column=self.clf_cnt + 5, sticky=NW)

    def change_winner_status(self, rule_cnt):
        if self.rules_dict[rule_cnt]['skip_on_equal_var'].get():
            self.rules_dict[rule_cnt]['winner_dropdown'].disable()
        else:
            self.rules_dict[rule_cnt]['winner_dropdown'].enable()


    def change_threshold_status(self, rule_cnt):
        if self.rules_dict[rule_cnt]['highest_var'].get():
            self.rules_dict[rule_cnt]['determinator_dropdown'].disable()
            self.rules_dict[rule_cnt]['threshold_entry'].set_state('disable')
            self.rules_dict[rule_cnt]['winner_dropdown'].enable()
            self.rules_dict[rule_cnt]['skip_on_equal_cb'].config(state=NORMAL)
        else:
            self.rules_dict[rule_cnt]['determinator_dropdown'].enable()
            self.rules_dict[rule_cnt]['threshold_entry'].set_state('normal')
            self.rules_dict[rule_cnt]['winner_dropdown'].disable()
            self.rules_dict[rule_cnt]['skip_on_equal_cb'].config(state=DISABLED)

    def run(self):
        rules = {}
        for rule_cnt, rule_data in self.rules_dict.items():
            rules[rule_cnt] = {}
            if not rule_data['highest_var']:
                rules[rule_cnt]['rule_type'] = 'threshold_determinator'
                check_float(name=f'Rule {rule_cnt+1}', value=rule_data['threshold_entry'].entry_get, max_value=1.00, min_value=0.00, raise_error=True)
                rule_determinator = rule_data['determinator_dropdown'].getChoices()
                rules[rule_cnt]['determinator'] = rule_determinator
                rules[rule_cnt]['threshold'] = float(rule_data['threshold_entry'].entry_get)
                rules[rule_cnt]['subordinates'] = []
                for subordinate_clf in rule_data['subordinates'].keys():
                    subordinate_rule = rule_data['subordinates'][subordinate_clf]['cb_var'].get()
                    if (rule_determinator == subordinate_clf) and (subordinate_rule is True):
                        raise DuplicationError(msg=f'In Rule {rule_cnt}, classifier {rule_determinator} is both a determinator and subordinate.')
                    if subordinate_rule:
                        rules[rule_cnt]['subordinates'].append(subordinate_clf)
                if len(rules[rule_cnt]['subordinates']) == 0:
                    NoSpecifiedOutputError(msg=f'Zero classifiers ticked for rule {rule_cnt}')

            else:
                rules[rule_cnt]['rule_type'] = 'highest_probability'
                rules[rule_cnt]['skip_files_with_identical'] = rule_data['skip_on_equal_var'].get()
                rules[rule_cnt]['subordinates'] = []
                for subordinate_clf in rule_data['subordinates'].keys():
                    subordinate_rule = rule_data['subordinates'][subordinate_clf]['cb_var'].get()
                    if subordinate_rule:
                        rules[rule_cnt]['subordinates'].append(subordinate_clf)
                if len(rules[rule_cnt]['subordinates']) < 2:
                    InvalidInputError(msg=f'Less than two classifiers ticked for rule #{rule_cnt}')
                if rule_data['winner_dropdown'].getChoices() not in rules[rule_cnt]['subordinates']:
                    InvalidInputError(msg=f'For rule {rule_cnt}, the winner ({rule_data["winner_dropdown"].getChoices()}) is not one of the checked classifiers.')
                else:
                    rules[rule_cnt]['winner'] = rule_data['winner_dropdown'].getChoices()

        corrector = MutualExclusivityCorrector(rules=rules, config_path=self.config_path)
        corrector.run()

#test = MutualExclusivityPupUp(config_path='/Users/simon/Desktop/envs/troubleshooting/anipose/project_folder/project_config.ini')


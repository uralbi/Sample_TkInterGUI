from FNS_data import staff, lead_email as ld


class FnsMail:
    def __init__(self):
        self.branches = ('LAO', 'LAGC','ATL', 'DFW', 'CHI','NYC', 'MIA', 'HOU', 'SFO')

    def staff_list(self, branch):
        for i, list in branch.items():
            print(i, f'({len(list)})')
            for name, email in list.items():
                print(f'{name}{" "*(16-len(name))}: {email}')

    def mailto_brn(self, branch):
        """
        :param branch: staff.branch_atl ...
        :return:
        """
        to = []
        cc = []
        for i, list in branch.items():
            if i =='TO':
                for mail in list.values():
                    to.append(mail)
            else:
                for mail in list.values():
                    cc.append(mail)
        print(f'TO:({len(to)})')
        for i in to:
            print(i, end=', ')
        print(f'\nCC:({len(cc)})')
        for i in cc:
            print(i,end=', ')
        print('\n')

    def plain_list(self, list):
        output = {}
        for k,v in list.items():
            output[k] = v
        for mail in output.values():
            print(mail, end=', ')

    def lead_to(self, list):
        """
        :param list: ['sbt', 'lot', 'fwt', 'soj', 'mch']
        :return:
        """
        em_to = []
        em_cc = []
        new_dc = {}
        for i in list:
            if i == 'sbt' or i == 'xf7':
                for k, v in ld.sbt.items():
                    if k == 'to':
                        for j in v:
                            em_to.append(j)
                    else:
                        for j in v:
                            em_cc.append(j)
                    # print(k, v)
            if i == 'lot':
                for k, v in ld.lot.items():
                    if k == 'to':
                        for j in v:
                            em_to.append(j)
                    else:
                        for j in v:
                            em_cc.append(j)
            if i == 'fwt':
                for k, v in ld.fwt.items():
                    if k == 'to':
                        for j in v:
                            em_to.append(j)
                    else:
                        for j in v:
                            em_cc.append(j)
            if i == 'soj':
                for k, v in ld.soj.items():
                    if k == 'to':
                        for j in v:
                            em_to.append(j)
                    else:
                        for j in v:
                            em_cc.append(j)
            if i == 'mch':
                for k, v in ld.mch.items():
                    if k == 'to':
                        for j in v:
                            em_to.append(j)
                    else:
                        for j in v:
                            em_cc.append(j)
        print('TO: ', '; '.join(em_to))
        print('CC: ', '; '.join(em_cc))


fns = FnsMail()
lead_l = ['sbt', 'lot', 'fwt', 'soj', 'mch']
# fns.lead_to(lead_l)

# fns.mailto_brn(staff.branch_atl)
# fns.staff_list(staff.branch_nyc)

branches = fns.branches
print(branches)

fns.staff_list(staff.branch_chi)

# fns.lead_to(['lot', 'fwt'])
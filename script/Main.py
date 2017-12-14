from DbManager import DbManager
from RatePredictor import RatePredictor

dbm = DbManager()

# for li in bank_currency:
# print(li,'\t',["%.3f" % v for v in  bank_currency[li]])
# '''

bank_cur_map = dbm.select_all()
nc_bank_cur_map = dbm.select_all_nb()

rpred = RatePredictor()
fcsts, mdls = rpred.predicted_values_all_banks(bank_cur_map)
# rpred.fcast_plots(fcsts)
rpred.model_plots(mdls, fcsts)

mt, mo, btails, boveralls = rpred.predicted_stat(fcsts)

print('\n', 'Min predicted course')
print('\n', 'bank : ', mt, '\n INFO :')
expected_min_tail = fcsts[mt]['trend'][-10:]
print(expected_min_tail)
print('\n', 'Min overal course for all time')
print('\n', 'bank : ', mo, '\n INFO :')
expected_min_overall = fcsts[mo]['trend']
print(expected_min_overall)

saved = rpred.saved_money(bank_cur_map, mo, 'Приорбанк', 2017, 11)
saved_with_bonus = rpred.saved_money_with_bonus(bank_cur_map, mo, 'Приорбанк', nc_bank_cur_map, 2017, 11)

print('\n', 'The best choice : ', mo)
print('saved money : ', saved, ' with bonus : ', saved_with_bonus)

dbm.conn.close()
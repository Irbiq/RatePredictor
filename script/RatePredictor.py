from collections import defaultdict
import pandas as pd
import fbprophet
import matplotlib.pyplot as plt

class RatePredictor:
    def predicted_stat(self, frcsts, periods=10):
        tail_sums = {}
        overall_sums = {}
        min_sum_tail = 99999999
        min_sum_overal = 9999999
        b_with_min_tail = ''
        b_with_min_overal = ''

        for bank in frcsts:
            s_t = frcsts[bank]['trend'][-periods:].sum()
            s_ov = frcsts[bank]['trend'].sum()
            tail_sums[bank] = s_t
            overall_sums[bank] = s_ov
            if (s_t < min_sum_tail):
                b_with_min_tail = bank
                min_sum_tail = s_t
            if (s_ov < min_sum_overal):
                b_with_min_overal = bank
                min_sum_overal = s_ov
        return b_with_min_tail, b_with_min_overal, tail_sums, overall_sums

    def predicted_values(self, bank_name, time_usd, periods=10, freq='1d'):
        proph_df = pd.DataFrame(list(time_usd.items()), columns=['ds', 'y'])
        model = fbprophet.Prophet(yearly_seasonality=False, daily_seasonality=False, weekly_seasonality=False)
        model.fit(proph_df);
        future = model.make_future_dataframe(periods=periods, freq=freq)
        forecast = model.predict(future)
        # print(bank_name)
        # print(proph_df.head())
        # print(forecast.head())
        # model.plot(forecast)
        return bank_name, forecast, model

    def predicted_values_all_banks(self, bank_cur_map):
        pred_values = {}
        models = {}
        for b_name, exchs in bank_cur_map.items():
            bname, forecast, model = self.predicted_values(b_name, exchs)
            pred_values[bname] = forecast
            models[bname] = model
        return pred_values, models

    def fcast_plot(self, forecast, real=list()):
        forecast.plot()
        plt.show()

    def fcast_plots(self, pred_values):
        for bank, forecast in pred_values.items():
            forecast.plot()
            plt.show()# ylabel = bank+': USD',xlabel = 'date'

    def model_plots(self, models, forecasts):
        i=0
        j=0
        k=1
        fig, axes = plt.subplots(nrows=8, ncols=3, sharex=True, sharey=True)
        for bank in models:
            models[bank].plot(forecasts[bank],ax=axes[i,j], ylabel=bank + ': USD', xlabel='date')
            if i == 7:
                j+=1
            i=(i+1)%8
            k=k+1
        print(k)
        plt.show()

    def saved_money(self, bank_cur_map, optimal_bank, compared_bank, year, month):
        exchs_comp = bank_cur_map[compared_bank]
        exchs_opt = bank_cur_map[optimal_bank]
        total_comp = 0
        total_opt = 0
        for t, usd in exchs_comp.items():
            if (t.year == year and t.month == month):
                total_comp += usd
        for t, usd in exchs_opt.items():
            if (t.year == year and t.month == month):
                total_opt += usd
        return (total_comp - total_opt) * 10000

    def saved_money_with_bonus(self, bank_cur_map, optimal_bank, compared_bank, exchs_nac_bank, year, month):
        exchs_comp = bank_cur_map[compared_bank]
        exchs_opt = bank_cur_map[optimal_bank]
        total_comp = 0
        total_opt = 0
        total_nb = 0
        for t, usd in exchs_comp.items():
            if (t.year == year and t.month == month):
                total_comp += usd
        for t, usd in exchs_opt.items():
            if (t.year == year and t.month == month):
                total_opt += usd
        for t, usd in exchs_nac_bank.items():
            if (t.year == year and t.month == month):
                total_nb += usd

        return (total_comp - total_opt + (total_opt - total_nb)) * 10000
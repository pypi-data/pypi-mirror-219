# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 07:47:19 2023

@author: varun
"""

"""
def iv_solver(index = True, method = ['ensemble', 'straddle', 'put'], front_back = ['front', 'back'], next_contract_skip = 3, interpolate = False, interpolate_term = 0, index_opt = 'weekly')



"""
    
import pandas as pd
import numpy as np
import datetime as dt



def straddle_iv_finder(straddle_price, spot, dte):
    """
    Returns implied volatility using the straddle approximation formula.

    Parameters
    ----------
    straddle_price : FLOAT
        ATM Straddle price.
    spot : FLOAT
        Spot or forward price (use spot if fewer than 7-10 days to expiry).
    dte : INT
        Days to expiry (will be converted to years)

    Returns
    ------_
    sigma : FLOAT
        Returns annualized implied volatility

    """
    
    sigma = (1.25*straddle_price)/(spot*np.sqrt(dte/365))
    return sigma

def find_liquid_strike(opt_bhav, expiry_date_str, strike_series, initial_guess, straddle=True, opt_type = 'p'):
    opt_type = (opt_type+'e').upper()
   
    final_price = np.nan
    if straddle:
        initial_straddle = opt_bhav[(opt_bhav['STRIKE_PR']==initial_guess)&(opt_bhav['EXPIRY_DT']==expiry_date_str)]
        if ((initial_straddle[['OPEN','HIGH','LOW']]==0).sum().sum()<1)&((initial_straddle['CHG_IN_OI']==0).sum() == 0): # filter for illiquidity
            final_price = initial_straddle['SETTLE_PR'].sum()
            final_strike = initial_guess
        else:
            strike_series_sorted = strike_series.sort_values()
            for i in range(1,10):
                next_strike = strike_series_sorted.index[i]
                next_straddle = opt_bhav[(opt_bhav['STRIKE_PR']==next_strike)&(opt_bhav['EXPIRY_DT']==expiry_date_str)]
                if ((next_straddle[['OPEN','HIGH','LOW']]==0).sum().sum()<1)&((next_straddle['CHG_IN_OI']==0).sum() == 0): # filter for illiquidity
                    final_strike = next_strike
                    final_price = next_straddle['SETTLE_PR'].sum()
                    break
                
        return final_price
    
    if not straddle:
        initial_price = opt_bhav[(opt_bhav['STRIKE_PR']==initial_guess)&(opt_bhav['EXPIRY_DT']==expiry_date_str)&(opt_bhav['OPTION_TYP']==opt_type)]
        if ((initial_price[['OPEN','HIGH','LOW']]==0).sum().sum()<1)&((initial_price['CHG_IN_OI']==0).sum() == 0): # filter for illiquidity
            final_price = initial_price['SETTLE_PR'].sum()
            final_strike = initial_guess
            
        else:
            strike_series_sorted = strike_series.sort_values()
            for i in range(1,10):
                next_strike = strike_series_sorted.index[i]
                next_price = opt_bhav[(opt_bhav['STRIKE_PR']==next_strike)&(opt_bhav['EXPIRY_DT']==expiry_date_str)&(opt_bhav['OPTION_TYP']==opt_type)]
                if ((next_price[['OPEN','HIGH','LOW']]==0).sum().sum()<1)&((next_price['CHG_IN_OI']==0).sum() == 0): # filter for illiquidity
                    final_strike = next_strike
                    final_price = next_price['SETTLE_PR'].sum()
                    break
         

        return final_price

def interpolate_iv(term, dte_near, dte_far, iv_near, iv_far):
    """
    Uses the interpolation formula used in the VIX white paper    

    Parameters
    ----------
    term : INT
        Number of days to interpolate (e.g. 30).
    dte_near : INT
        Days to expiry for the front contract.
    dte_far : INT
        Days to expiry for the rear contract.
    iv_near : FLOAT
        Implied volatility (in Percentage) of the front contract.
    iv_far : FLOAT
        Implied volatility (in Percentage) of the rear contract.

    Returns
    -------
    iv : FLOAT
    

    """
    
    iv_near = iv_near/100
    iv_far = iv_far/100
    tte_near = dte_near/365
    tte_far = dte_far/365
    tte_thirty = term/365

    iv = 100*np.sqrt((((tte_near*(iv_near**2))*((tte_far - tte_thirty)/(tte_far - tte_near)))+((tte_far*(iv_far**2))*((tte_thirty - tte_near)/(tte_far - tte_near))))*(365/30))
    return iv




def retrieve_iv(symbol, date, index = True, method = 'straddle', front_back = 'interpolate', next_contract_skip = 3, interpolate_term = 0):
    call_put_dict = {'put': 'p', 'call': 'c'}
    final_iv = np.nan
    try:
        date_str  = date.strftime('%Y-%m-%d')
        bhav = pd.read_csv(rf'C:\Users\varun\Documents\Raw Data\Bhavcopies\Bhavcopy_fno_{date_str}.csv')
        bhav = bhav[bhav['SYMBOL']==symbol]
        
        if index:   # filtering depending on index or single stock   
            fut_bhav = bhav[bhav['INSTRUMENT']=='FUTIDX']
            opt_bhav = bhav[bhav['INSTRUMENT']=='OPTIDX']
        else:
            fut_bhav = bhav[bhav['INSTRUMENT']=='FUTSTK']
            opt_bhav = bhav[bhav['INSTRUMENT']=='OPTSTK']
                    
        front_fut = fut_bhav['SETTLE_PR'].iloc[0]
        back_fut = fut_bhav['SETTLE_PR'].iloc[1]
                    
        front_expiry_date_str = fut_bhav['EXPIRY_DT'].iloc[0]
        front_expiry_date = dt.datetime.strptime(front_expiry_date_str, '%Y-%m-%d')
        back_expiry_date_str = fut_bhav['EXPIRY_DT'].iloc[1]
        back_expiry_date = dt.datetime.strptime(back_expiry_date_str, '%Y-%m-%d')
                            
        front_dte = (front_expiry_date - date).days
        back_dte = (back_expiry_date - date).days
        
        
        if front_back == 'front':
            if front_dte <= next_contract_skip: # This is rolling to the next contract
                front_expiry_date_str = back_expiry_date_str
                front_expiry_date = back_expiry_date
                front_dte = back_dte
                front_fut = back_fut
                
            strike_list = pd.Series(opt_bhav[opt_bhav['EXPIRY_DT']==front_expiry_date_str]['STRIKE_PR'].unique())
            front_strike_diff = abs(strike_list - front_fut) # finding the closest strikes to the forward
            front_strike_diff.index = strike_list
            front_closest_strike = front_strike_diff[front_strike_diff == front_strike_diff.min()].index[0]
            
            if method == 'straddle':
                front_month_straddle = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = True)
                final_iv = straddle_iv_finder(front_month_straddle, front_fut, front_dte)
            elif method == 'put':
                front_pe_price = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = False)
                final_iv = implied_vol(front_fut, front_closest_strike, front_dte/365, 0.07, front_pe_price, 'p')
            elif method == 'call':
                front_ce_price = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = False, opt_type = 'c')
                final_iv = implied_vol(front_fut, front_closest_strike, front_dte/365, 0.07, front_pe_price, 'c')
        
            else:
                front_month_straddle = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = True)
                front_straddle_iv = straddle_iv_finder(front_month_straddle, front_fut, front_dte)
                front_pe_price = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = False)
                front_pe_iv = implied_vol(front_fut, front_closest_strike, front_dte/365, 0.07, front_pe_price, 'p')
                front_ce_price = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = False, opt_type = 'c')
                front_ce_iv = implied_vol(front_fut, front_closest_strike, front_dte/365, 0.07, front_pe_price, 'c')
                
                final_iv = (front_ce_iv+ front_pe_iv + front_straddle_iv)/3
        
            
            return final_iv
       
        elif front_back == 'back':
            if back_dte <= next_contract_skip: # This is rolling to the next contract
                back_expiry_date_str = fut_bhav['EXPIRY_DT'].iloc[2]
                back_expiry_date = dt.datetime.strptime(back_expiry_date_str, '%Y-%m-%d')
                back_dte = (back_expiry_date - date).days
                back_fut = fut_bhav['SETTLE_PR'].iloc[2]
                
            strike_list = pd.Series(opt_bhav[opt_bhav['EXPIRY_DT']==back_expiry_date_str]['STRIKE_PR'].unique())
            back_strike_diff = abs(strike_list - back_fut) # finding the closest strikes to the forward
            back_strike_diff.index = strike_list
            back_closest_strike = back_strike_diff[back_strike_diff == back_strike_diff.min()].index[0]
            
            if method == 'straddle':
                back_month_straddle = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = True)
                final_iv = straddle_iv_finder(back_month_straddle, back_fut, back_dte)
            elif method == 'put':
                back_pe_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False)
                final_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_pe_price, 'p')
            elif method == 'call':
                back_ce_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = 'c')
                final_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_ce_price, 'c')
           
            else:
                back_month_straddle = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = True)
                back_straddle_iv = straddle_iv_finder(back_month_straddle, back_fut, back_dte)
                back_pe_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False)
                back_pe_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_pe_price, 'p')
                back_ce_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = 'c')
                back_ce_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_ce_price, 'c')
               
                final_iv = (back_ce_iv+ back_pe_iv + back_straddle_iv)/3
        
            return final_iv
        
        
        else: # when front_back == 'interpolate'
            strike_list = pd.Series(opt_bhav[opt_bhav['EXPIRY_DT']==front_expiry_date_str]['STRIKE_PR'].unique())
            front_strike_diff = abs(strike_list - front_fut) # finding the closest strikes to the forward
            front_strike_diff.index = strike_list
            front_closest_strike = front_strike_diff[front_strike_diff == front_strike_diff.min()].index[0]
                
            strike_list = pd.Series(opt_bhav[opt_bhav['EXPIRY_DT']==back_expiry_date_str]['STRIKE_PR'].unique())
            back_strike_diff = abs(strike_list - back_fut) # finding the closest strikes to the forward
            back_strike_diff.index = strike_list
            back_closest_strike = back_strike_diff[back_strike_diff == back_strike_diff.min()].index[0]
            
        
            if method == 'straddle':
                if front_dte > 0:
                    front_month_straddle = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = True)
                    front_straddle_iv = straddle_iv_finder(front_month_straddle, front_fut, front_dte)
                    back_month_straddle = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = True)
                    back_straddle_iv = straddle_iv_finder(back_month_straddle, back_fut, back_dte)
                    if back_month_straddle != np.nan:
                        final_iv = interpolate_iv(interpolate_term, front_dte, back_dte, front_straddle_iv, back_straddle_iv)
                    else:
                        final_iv = front_straddle_iv
                
                else:
                    final_iv = straddle_iv_finder(back_month_straddle, back_fut, back_dte)
                    
                    
            if method in ['put', 'call']:
                if front_dte > 0:
                    front_price = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = False, opt_type = call_put_dict[method])
                    front_iv = implied_vol(front_fut, front_closest_strike, front_dte/365, 0.07, front_price, call_put_dict[method])
                    back_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = call_put_dict[method])
                    back_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_price, call_put_dict[method])
                    
                    if back_price != np.nan:
                        final_iv = interpolate_iv(interpolate_term, front_dte, back_dte, front_iv, back_iv)
                    else:
                        final_iv = front_iv
                
                else:
                    back_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = call_put_dict[method])
                    final_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_price, call_put_dict[method])
            
            
            if method == 'ensemble':
                if front_dte > 0:
                    front_month_straddle = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = True)
                    front_straddle_iv = straddle_iv_finder(front_month_straddle, front_fut, front_dte)
                    back_month_straddle = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = True)
                    back_straddle_iv = straddle_iv_finder(back_month_straddle, back_fut, back_dte)
                    if back_month_straddle != np.nan:
                        interpolated_straddle_iv = interpolate_iv(interpolate_term, front_dte, back_dte, front_straddle_iv, back_straddle_iv)
                    else:
                        interpolated_straddle_iv = front_straddle_iv
                
                else:
                    front_straddle_iv = straddle_iv_finder(back_month_straddle, back_fut, back_dte)
                    interpolated_straddle_iv = front_straddle_iv
            
        
               
                if front_dte > 0:
                    front_price = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = False, opt_type = call_put_dict['call'])
                    front_iv = implied_vol(front_fut, front_closest_strike, front_dte/365, 0.07, front_price, call_put_dict['call'])
                    back_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = call_put_dict['call'])
                    back_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_price, call_put_dict['call'])
                    
                    if back_price != np.nan:
                        interpolated_call_iv = interpolate_iv(interpolate_term, front_dte, back_dte, front_iv, back_iv)
                    else:
                        interpolated_call_iv = front_iv
                
                else:
                    back_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = call_put_dict['call'])
                    interpolated_call_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_price, call_put_dict['call'])
            
            
               
                if front_dte > 0:
                    front_price = find_liquid_strike(opt_bhav, front_expiry_date_str, front_strike_diff, front_closest_strike, straddle = False, opt_type = call_put_dict['put'])
                    front_iv = implied_vol(front_fut, front_closest_strike, front_dte/365, 0.07, front_price, call_put_dict['put'])
                    back_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = call_put_dict['put'])
                    back_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_price, call_put_dict['put'])
                    
                    if back_price != np.nan:
                        interpolated_put_iv = interpolate_iv(interpolate_term, front_dte, back_dte, front_iv, back_iv)
                    else:
                        interpolated_put_iv = front_iv
                
                else:
                    back_price = find_liquid_strike(opt_bhav, back_expiry_date_str, back_strike_diff, back_closest_strike, straddle = False, opt_type = call_put_dict['put'])
                    interpolated_put_iv = implied_vol(back_fut, back_closest_strike, back_dte/365, 0.07, back_price, call_put_dict['put'])
            
                
                
                final_iv = (interpolated_straddle_iv + interpolated_call_iv + interpolated_put_iv)/3
                
            return final_iv
    except Exception as e:
        return final_iv
        print(f'error {e} for {date} for {symbol}')

retrieve_iv('RELIANCE', dt.datetime(2023,7,10), False, front_back = 'back', method = 'put')

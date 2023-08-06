#######
# FARMS
#######

def buyFarm(buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Farm',
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Buy Farm'
    }

def upgradeFarm(index, path, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Upgrade Farm',
        'Index': index,
        'Path': path,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Upgrade farm %s at path %s'%(index, path) 
    }

def sellFarm(index, min_buy_time = 0, withdraw = False):
    #Look, I know this is confusing, but "min_buy_time" really is the minimum selling time in this case!
    return {
        'Type': 'Sell Farm',
        'Index': index,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Sell farm %s'%(index),
        'Withdraw': withdraw
    }

def buyDefense(cost, buffer = 0, min_buy_time = 0, message = 'Buy Defense'):
    return {
        'Type': 'Buy Defense',
        'Cost': cost,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': message
    }

def withdrawBank(index, min_buy_time = 0):
    return {
        'Type': 'Withdraw Bank',
        'Index': index,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Withdraw from farm %s'%(index)
    }

def activateIMF(index, min_buy_time = 0):
    return {
        'Type': 'Activate IMF',
        'Index': index,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Take out loan from farm %s'%(index)
    }

def sellAllFarms(min_buy_time = 0, withdraw = False):
    return {
        'Type': 'Sell All Farms',
        'Minimum Buy Time': min_buy_time,
        'Withdraw': withdraw #Okay, this might be confusing, but this is actually the minimum *sell* time for this action.
    }

# WARNING: This function is for declaring farms in the initial game state. 
# Do NOT use it to add farms during simulation
def initFarm(purchase_time = None, upgrades = [0,0,0]):
    return {
        'Purchase Time': purchase_time,
        'Upgrades': upgrades,
        'Account Value': 0
    }

############
# BOAT FARMS
############

def buyBoatFarm(buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Boat Farm',
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Buy boat farm'
    }

def upgradeBoatFarm(index, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Upgrade Boat Farm',
        'Index': index,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Upgrade boat farm at index %s'%(index)
    }

def sellBoatFarm(index, min_buy_time = 0):
    #Look, I know this is confusing, but "min_buy_time" really is the minimum selling time in this case!
    return {
        'Type': 'Sell Boat Farm',
        'Index': index,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Sell boat farm %s'%(index)
    }

#Not yet implemented, don't use
def sellAllBoatFarms(min_buy_time = 0):
    return {
        'Type': 'Sell All Boat Farms',
        'Minimum Buy Time': min_buy_time #Okay, this might be confusing, but this is actually the minimum *sell* time for this action.
    }

# WARNING: This function is for declaring boat farms in the initial game state. 
# Do NOT use it to add boat farms during simulation
def initBoatFarm(purchase_time = None, upgrade = 3):
    return {
        'Initial Purchase Time': purchase_time,
        'Purchase Time': purchase_time,
        'Upgrade': upgrade,
        'Revenue': 0,
        'Expenses': 0,
        'Hypothetical Revenue': 0,
        'Sell Time': None
    }

#############
# DRUID FARMS
#############

def buyDruidFarm(buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Druid Farm',
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Buy druid farm'
    }

def buySOTF(index, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Spirit of the Forest',
        'Index': index, 
        'Buffer': buffer, 
        'Minimum Buy Time': min_buy_time,
        'Message': 'Upgrade druid farm %s to SOTF'%(index)
    }

def sellDruidFarm(index, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Sell Druid Farm',
        'Index': index,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Sell druid farm %s'%(index)
    }

def repeatedlyBuyDruidFarms(min_buy_time = 0, max_buy_time = float('inf'), max_amount = None, buffer = 0):
    return {
        'Type': 'Repeatedly Buy Druid Farms',
        'Minimum Buy Time': min_buy_time,
        'Maximum Buy Time': max_buy_time,
        'Maximum Amount': max_amount,
        'Buffer': buffer,
        'Message': 'Trigger repeated druid farm buys until time %s'%(max_buy_time)
    }

#Not yet implemented, don't use
def sellAllDruidFarms(min_buy_time = 0):
    return {
        'Type': 'Sell All Druid Farms',
        'Minimum Buy Time': min_buy_time #Okay, this might be confusing, but this is actually the minimum *sell* time for this action.
    }

# WARNING: This function is for declaring druid farms in the initial game state. 
# Do NOT use it to add druid farms during simulation
def initDruidFarms(purchase_times, sotf = None):
    dictionary = {}
    for i in range(len(purchase_times)):
        dictionary[i] = purchase_times[i]
    dictionary['Spirit of the Forest Index'] = sotf
    return dictionary

##############
# SUPPLY DROPS
##############

def buySupplyDrop(buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Supply Drop',
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Buy supply drop'
    }

def buyEliteSniper(index, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Elite Sniper',
        'Index': index,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Upgrade supply drop %s to e-sniper'%(index)
    }

def sellSupplyDrop(index, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Sell Supply Drop',
        'Index': index,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Sell supply drop %s'%(index)
    }

def repeatedlyBuySupplyDrops(min_buy_time = 0, max_buy_time = float('inf'), max_amount = None, buffer = 0):
    return {
        'Type': 'Repeatedly Buy Supply Drops',
        'Minimum Buy Time': min_buy_time,
        'Maximum Buy Time': max_buy_time,
        'Maximum Amount': max_amount,
        'Buffer': buffer,
        'Message': 'Trigger repeated supply drop buys until time %s'%(max_buy_time)
    }

#Not yet implemented, don't use
def sellAllSupplyDrops(min_buy_time = 0):
    return {
        'Type': 'Sell All Supply Drops',
        'Minimum Buy Time': min_buy_time #Okay, this might be confusing, but this is actually the minimum *sell* time for this action.
    }

# WARNING: This function is for declaring supply drops in the initial game state. 
# Do NOT use it to add supply drops during simulation
def initSupplyDrops(purchase_times, elite_sniper = None):
    dictionary = {}
    for i in range(len(purchase_times)):
        dictionary[i] = purchase_times[i]
    dictionary['Elite Sniper Index'] = elite_sniper
    return dictionary

############
# HELICOPTER
############

def buyHeliFarm(buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Heli Farm',
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Buy heli farm'
    }

def buySpecialPoperations(index, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Buy Special Poperations',
        'Index': index,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Upgrade heli farm %s to x5x'%(index)
    }

def sellHeliFarm(index, buffer = 0, min_buy_time = 0):
    return {
        'Type': 'Sell Heli Farm',
        'Index': index,
        'Buffer': buffer,
        'Minimum Buy Time': min_buy_time,
        'Message': 'Sell heli farm %s'%(index)
    }

def repeatedlyBuyHeliFarms(min_buy_time = 0, max_buy_time = float('inf'), max_amount = None, buffer = 0):
    return {
        'Type': 'Repeatedly Buy Heli Farms',
        'Minimum Buy Time': min_buy_time,
        'Maximum Buy Time': max_buy_time,
        'Maximum Amount': max_amount,
        'Buffer': buffer,
        'Message': 'Trigger repeated heli farm buys until time %s'%(max_buy_time)
    }

#Not yet implemented, don't use
def sellAllHeliFarms(min_buy_time = 0):
    return {
        'Type': 'Sell All Heli Farms',
        'Minimum Buy Time': min_buy_time #Okay, this might be confusing, but this is actually the minimum *sell* time for this action.
    }

# WARNING: This function is for declaring heli farms in the initial game state. 
# Do NOT use it to add supply drops during simulation
def initHeliFarms(purchase_times, special_poperations = None):
    dictionary = {}
    for i in range(len(purchase_times)):
        dictionary[i] = purchase_times[i]
    dictionary['Special Poperations Index'] = special_poperations
    return dictionary

#################
# JERICHO ACTIONS
#################

def jerichoSteal(min_buy_time = 0, steal_amount = 25):
    return {
        'Type': 'Jericho Steal',
        'Minimum Buy Time': min_buy_time,
        'Steal Amount': steal_amount,
        'Message': 'Trigger Jericho Steal'
    }

###########
# ECO QUEUE
###########

def ecoSend(time = None, send_name = 'Zero', property = 'Normal', max_send_amount = None, max_eco_amount = None, max_send_time = None, queue_threshold = 6):
    
    fortified = False
    camo = False
    regrow = False

    if property == 'Fortified':
        fortified = True
    elif property == 'Camo':
        camo = True
    elif property == 'Regrow':
        regrow = True
    

    elif property == 'Fortified Camo':
        fortified = True
        camo = True
    elif property == 'Fortified Regrow':
        fortified = True
        regrow = True
    elif property == 'Camo Regrow':
        camo = True
        regrow = True
    
    elif property == 'Fortified Camo Regrow':
        fortified = True
        camo = True
        regrow = True

    return {
        'Time': time,
        'Send Name': send_name,
        'Max Send Amount': max_send_amount,
        'Fortified': fortified,
        'Camoflauge': camo,
        'Regrow': regrow,
        'Max Eco Amount': max_eco_amount,
        'Max Send Time': max_send_time,
        'Queue Threshold': queue_threshold
    }
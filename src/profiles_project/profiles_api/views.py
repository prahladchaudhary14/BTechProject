from django.shortcuts import render
from .import serializers
from rest_framework import status

# Create your views here.
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from . import models
from .import permissions
from rest_framework.authentication import TokenAuthentication
import random
import datetime

"""Note: Use 24 Hour Clock for the code to work"""

"""
PRINTED VALUES CORRESPONDING TO THE VARIABLES
DC -> dc
SG -> sg
AG -> ag
Frequency -> frequency
Fuel Price -> fuel_price
Current Block Number -> current_block_number
Current Block Time -> current_block
Next Block Time -> next_block
Time Elapsed -> time_elapsed
Time Remaining -> Time Remaining
"""

null=0;
class PowerPlantData(APIView):
    """Test API View"""
    def get(self, request, format=None):
        """Returns a list of api view features"""

        """
        Notes:
        **Use 24 Hour Clock for the code to work**
        Don't use f-strings (not compatible with python version < 3.6)
        """

        """
        PRINTED VALUES CORRESPONDING TO THE VARIABLES
        (Updated every second):
        Time Elapsed -> time_elapsed
        Time Remaining -> Time Remaining
        (Updated every 15 minutes):
        DC -> dc
        SG -> sg
        AG -> ag
        Frequency -> frequency
        Current Block Number -> current_block_number
        Current Block Time -> current_block
        Next Block Time -> next_block
        Values under #Charges -> same as the jupyter file
        Next Block's sg -> sg_plus_one
        Next to Next block's sg -> sg_plus_two
        and so on... -> sg_plus_three, sg_plus_four
        (Updated every day)
        Fuel Price -> fuel_price
        """


        # Returns starting minute of the block
        def function(time_m: str, blk: str = 'n') -> str:
            if blk == 'p':
                block_region = int(time_m) // 15 + 1
                op = (block_region - 1) * 15
                return str(op) * 2 if 1 == len(str(op)) else str(op)
            else:
                op = str(((int(time_m) // 15 + 1) * 15) % 60)
                return op * 2 if 1 == len(op) else op


        # Takes digit in int form and converts it to two digits (if only one) by adding preceding zero, returns str
        def digit_convert(number: int) -> str:
            if len(str(number)) == 1:
                return '0' + str(number)
            else:
                return str(number)


        # Takes a block number and returns a number between 1 and 96 i.e. converts block 97 to block 1, etc.
        def block_number(n):
            if n > 96:
                return n % 96
            else:
                return n


        # Defines the seed input for random functions (for 15 minute values)
        def function_seed(blk_no, day, mon):
            return (96 * 96) * blk_no + 96 * day + mon


        # Defines the seed input for random functions (for 1 day values)
        def function_seed_day(day, mon):
            return 32 * day + mon


        # Take frequency as input and output the deviation rate
        def deviation_rate(f):
            if 49.48 <= f <= 50.00:
                return 3.0304
            elif f == 50.01:
                return 2.5063
            elif f == 50.02:
                return 1.8798
            elif f == 50.03:
                return 1.2532
            elif f == 50.04:
                return 0.6266
            else:
                return 0


        def ui_dev_charge_calculate(dev, f, rs):
            if dev <= 0 and f >= 49.85:
                return round(rs * dev * f, 2)
            else:
                return 0


        def ui_charge_above_and_150_calculate(dev, f, s, a, rs):
            if f >= 49.85 and 0.12 * s <= 150:
                if 0.85 * s <= a < 0.88 * s:
                    return round(-1 * 50 * (-dev - 0.12 * s), 2)
                elif 0.8 * s <= a < 0.85 * s:
                    return round((-1 * (100 * (-dev - 0.15 * s) + 1.5 * s)) * rs, 2)
                else:
                    return round((-1 * (250 * (-dev - 0.2 * s) + 6.5 * s)) * rs, 2)
            else:
                return 0


        def ui_dev_charge_above_and_012_calculate(dev, f, s, rs):
            if f >= 49.85 and 0.12 * s > 150:
                if 150 < dev <= 200:
                    return round((- 1 * (50 * (- dev - 150)) * rs), 2)
                elif 200 < -dev <= 250:
                    return round((- 1 * (100 * (-dev - 200) + 2500) * rs), 2)
                elif -dev > 250:
                    return round((- 1 * (250 * (- dev - 250) + 7500)) * rs, 2)
                else:
                    return 0
            else:
                return 0


        def ui_dev_charge_below_dc_calculate(dev, f, s, a, rs):
            if a <= s and f < 49.85:
                return round(dev * rs * 250, 2)
            else:
                return 0


        def ui_dev_charge_below_dc_add_calculate(dev, f, s, a, rs):
            if a <= s and f < 49.85:
                return round(dev * rs * 250, 2)
            else:
                return 0


        def oi_dev_charge_calculate(dev, s, a, rs):
            if a > s and dev > 0.12 * s and 0.12 * s < 150:
                return round(0.12 * s * rs * 250, 2)
            elif a > s and dev < s * 0.12 and dev < 150:
                return round(dev * rs * 250, 2)
            elif a > s and 0.12 * s > 150:
                return round(150 * rs * 250, 2)
            elif a > s and 0.12 * s < 150:
                return round(0.12 * s * rs * 250, 2)
            else:
                return 0


        def oi_dev_charge_add_calculate(dev, f, s, a):
            if a > s > 400 and f >= 50.1:
                return round(dev * 250 * min(50.03, 0) / 100, 2)
            elif a > s and s <= 400 and f >= 50.1 and dev > 48:
                return round((dev - 48) * 250 * min(50.03, 0) / 100, 2)
            else:
                return 0


        """Read time from the system clock, using that, Assign current block number, current block and next block """
        t = str(datetime.datetime.now().time())
        t_hh, t_mm, t_ss = t[:2], t[3:5], t[6:8]
        current_block_place = int(t_mm) // 15 + 1
        next_block_place = 1 if current_block_place == 4 else current_block_place + 1

        current_block_number = (int(t_hh) * 60 + int(t_mm)) // 15 + 1
        current_block_start = t_hh + ":" + digit_convert((int(t_mm) // 15) * 15)
        next_block_start = digit_convert(((int(t_hh) + 1) % 24) if current_block_place == 4 else t_hh) + ":" + function(t_mm)
        current_block_end = next_block_start
        next_block_end = digit_convert((int(next_block_start[:2]) + 1) % 24) + ":" + "00" if next_block_place == 4 else digit_convert(int(next_block_start[:2])) + ":" + digit_convert(int(next_block_start[-2:]) + 15)

        current_block = current_block_start + "-" + current_block_end
        next_block = next_block_start + "-" + next_block_end

        """From the time (used above) find the time elapsed and the time remaining"""
        time_elapsed_mm, time_elapsed_ss = digit_convert(int(t_mm) % 15), digit_convert(int(t_ss))
        time_remaining_in_seconds = digit_convert(15 * 60 - (int(time_elapsed_mm) * 60 + int(time_elapsed_ss)))
        time_remaining_mm, time_remaining_ss = digit_convert(int(time_remaining_in_seconds) // 60), digit_convert(int(time_remaining_in_seconds) % 60)

        time_elapsed = time_elapsed_mm + ":" + time_elapsed_ss
        time_remaining = time_remaining_mm + ":" + time_remaining_ss

        # Date calculation (used in seeding of random functions)
        date = str(datetime.date.today())
        date_day = int(date[-2:])
        date_mon = int(date[-5:-3])

        """Randomizing the values as per the specified ranges"""
        random.seed(function_seed(block_number(current_block_number), date_day, date_mon))
        # Update in intervals of 15 minutes (1 time block)
        dc = round(150 + random.random() * 50, 2)
        sg = round(150 + random.random() * 50, 2)
        ag = round(150 + random.random() * 50, 2)
        frequency = round(49.5 + random.random() * 1.5, 2)
        deviation = ag - sg

        rupees = deviation_rate(frequency)


        # Charges
        ui_dev_charge = ui_dev_charge_calculate(deviation, frequency, rupees)
        ui_dev_charge_above_and_150 = ui_charge_above_and_150_calculate(deviation, frequency, sg, ag, rupees)
        ui_dev_charge_above_and_012 = ui_dev_charge_above_and_012_calculate(deviation, frequency, sg, rupees)
        ui_dev_charge_below_dc = ui_dev_charge_below_dc_calculate(deviation, frequency, sg, ag, rupees)
        ui_dev_charge_below_dc_add = ui_dev_charge_below_dc_add_calculate(deviation, frequency, sg, ag, rupees)
        oi_dev_charge = oi_dev_charge_calculate(deviation, sg, ag, rupees)
        oi_dev_charge_add = oi_dev_charge_add_calculate(deviation, frequency, sg, ag)

        sum_ui = ui_dev_charge + ui_dev_charge_above_and_150 + ui_dev_charge_above_and_012 + ui_dev_charge_below_dc + ui_dev_charge_below_dc_add
        total_charge = sum_ui + oi_dev_charge + oi_dev_charge_add
        total_charge_add = ui_dev_charge_above_and_150 + ui_dev_charge_above_and_012 + ui_dev_charge_below_dc_add + oi_dev_charge_add

        fuel = deviation * 250 * 151.4 / 100 * (-1)
        net_gain = fuel + total_charge


        "Previous Block Number and Time"
        previous_block_number = 96 if current_block_number == 1 else current_block_number - 1

        previous_block_end = current_block_start

        # ----
        previous_block_start_mm = digit_convert((int(previous_block_end[-2:]) - 15) % 60)
        previous_block_start_hh = digit_convert(int(t_hh) - 1) if current_block_place == 1 else t_hh
        # ----

        previous_block_start = previous_block_start_hh + ":" + previous_block_start_mm

        previous_block = previous_block_start + "-" + previous_block_end

        """Previous Block Data"""
        # Same parameters calculated; Added a 'previous_' prefix to differentiate

        random.seed(function_seed(current_block_number - 1, date_day, date_mon))
        previous_dc = round(150 + random.random() * 50, 2)
        previous_sg = round(150 + random.random() * 50, 2)
        previous_ag = round(150 + random.random() * 50, 2)
        previous_frequency = round(49.5 + random.random() * 1.5, 2)
        previous_deviation = previous_ag - previous_sg
        previous_rupees = deviation_rate(previous_frequency)

        previous_ui_dev_charge = ui_dev_charge_calculate(previous_deviation, previous_frequency, previous_rupees)
        previous_oi_dev_charge = oi_dev_charge_calculate(previous_deviation, previous_sg, previous_ag, previous_rupees)

        previous_ui_dev_charge_above_and_150 = ui_charge_above_and_150_calculate(previous_deviation, previous_frequency, previous_sg, previous_ag, previous_rupees)
        previous_ui_dev_charge_above_and_012 = ui_dev_charge_above_and_012_calculate(previous_deviation, previous_frequency, previous_sg, previous_rupees)

        previous_ui_dev_charge_below_dc = ui_dev_charge_below_dc_calculate(previous_deviation, previous_frequency, previous_sg, previous_ag, previous_rupees)

        previous_ui_dev_charge_below_dc_add = ui_dev_charge_below_dc_add_calculate(previous_deviation, previous_frequency, previous_sg, previous_ag, previous_rupees)
        previous_oi_dev_charge_add = oi_dev_charge_add_calculate(previous_deviation, previous_frequency, previous_sg, previous_ag)


        previous_sum_ui = previous_ui_dev_charge + previous_ui_dev_charge_above_and_150 + previous_ui_dev_charge_above_and_012 + previous_ui_dev_charge_below_dc + previous_ui_dev_charge_below_dc_add

        previous_total_charge = previous_sum_ui + previous_oi_dev_charge + previous_oi_dev_charge_add
        previous_total_charge_add = previous_ui_dev_charge_above_and_150 + previous_ui_dev_charge_above_and_012 + previous_ui_dev_charge_below_dc_add + previous_oi_dev_charge_add

        previous_fuel = previous_deviation * 250 * 151.4 / 100 * (-1)
        previous_net_gain = previous_fuel + previous_total_charge


        # SG for the next four blocks
        random.seed(function_seed(block_number(current_block_number + 1), date_day, date_mon))
        sg_plus_one = round(150 + random.random() * 50, 2)

        random.seed(function_seed(block_number(current_block_number + 2), date_day, date_mon))
        sg_plus_two = round(150 + random.random() * 50, 2)

        random.seed(function_seed(block_number(current_block_number + 3), date_day, date_mon))
        sg_plus_three = round(150 + random.random() * 50, 2)

        random.seed(function_seed(block_number(current_block_number + 4), date_day, date_mon))
        sg_plus_four = round(150 + random.random() * 50, 2)

        # Updated every 24 hours
        random.seed(function_seed_day(date_day, date_mon))
        fuel_price = round(2 + random.random() * 8, 2)
        return Response({
           "Dc":dc,
           "Sg":sg,
           "Ag":ag,
           "Frequency":frequency,
           "FuelPrice":fuel_price,
           "DeviationRate":rupees,
           "Deviation":deviation,
           "Deviation_Rs":total_charge,
           "AdditionalDeviationCharge":total_charge_add,
           "FuelCost":fuel,
           "NetGain":net_gain,
           "SgPlusOne":sg_plus_one,
           "SgPlusTwo":sg_plus_two,
           "SgPlusThree":sg_plus_three,
           "SgPlusFour":sg_plus_four,
           "PreviousBlockNumber":previous_block_number,
           "PreviousBlock":previous_block,
           "PreviousDc":previous_dc,
           "PreviousSg":previous_sg,
           "PreviousFrequency":previous_frequency,
           "PreviousDeviation":previous_deviation,
           "PreviousDeviationRate":previous_rupees,
           "PreviousDeviationRupees":previous_total_charge,
           "PreviousAdditionalDeviationCharge":previous_total_charge_add,
           "PreviousFuelCost":previous_fuel,
           "PreviousNetGain":previous_net_gain,
            })
class TimeData(APIView):
    """Test API View"""
    def get(self, request, format=None):
        """Returns a list of api view features"""

        def function(time_m: str, blk: str = 'n') -> str:
            if blk == 'p':
                block_region = int(time_m) // 15 + 1
                op = (block_region - 1) * 15
                return str(op) * 2 if 1 == len(str(op)) else str(op)
            else:
                op = str(((int(time_m) // 15 + 1) * 15) % 60)
                return op * 2 if 1 == len(op) else op
        # Takes digit in int form and converts it to two digits (if only one) by adding preceding zero, returns str
        def digit_convert(number: int) -> str:
            if len(str(number)) == 1:
                return '0' + str(number)
            else:
                return str(number)


        t = str(datetime.datetime.now().time())
        t_hh, t_mm, t_ss = t[:2], t[3:5], t[6:8]
        current_block_place = int(t_mm) // 15 + 1
        next_block_place = 1 if current_block_place == 4 else current_block_place + 1

        current_block_number = (int(t_hh) * 60 + int(t_mm)) // 15 + 1
        current_block_start = t_hh + ":" + digit_convert((int(t_mm) // 15) * 15)
        next_block_start = digit_convert(((int(t_hh) + 1) % 24) if current_block_place == 4 else t_hh) + ":" + function(t_mm)
        current_block_end = next_block_start
        next_block_end = digit_convert((int(next_block_start[:2]) + 1) % 24) + ":" + "00" if next_block_place == 4 else digit_convert(int(next_block_start[:2])) + ":" + digit_convert(int(next_block_start[-2:]) + 15)

        current_block = current_block_start + "-" + current_block_end
        next_block = next_block_start + "-" + next_block_end

        """Code to find time elapsed and time remaining"""

        time_elapsed_mm, time_elapsed_ss = digit_convert(int(t_mm) % 15), digit_convert(int(t_ss))
        time_remaining_in_seconds = digit_convert(15 * 60 - (int(time_elapsed_mm) * 60 + int(time_elapsed_ss)))
        time_remaining_mm, time_remaining_ss = digit_convert(int(time_remaining_in_seconds) // 60), digit_convert(int(time_remaining_in_seconds) % 60)

        time_elapsed = time_elapsed_mm + ":" + time_elapsed_ss
        time_remaining = time_remaining_mm+":"+time_remaining_ss



        """"
        Code for updating the variables follow:
        Update after time interval: All updated when time advances to the next time block
        Fuel Price is updated only when the day changes i.e. at Time Block 1
        """

        """
        Detects the start of the next block then starts updating values every 15 minutes
        else waits for 1 minute and checks again
        """

        """Initialization"""
        random.seed(int(current_block_start[:2]) + int(current_block_start[3:5]))
        # Update in intervals of 15 minutes (1 time block)
        dc = round(150 + random.random() * 50, 2)
        sg = round(150 + random.random() * 50, 2)
        ag = round(150 + random.random() * 50, 2)

        frequency = round(49.5 + random.random() * 1.5, 2)

        # Updated every 24 hours
        random.seed(int(str(datetime.date.today())[-2:]))
        fuel_price = round(2 + random.random() * 8, 2);
        return Response({
          "CurrentBlockNumber":current_block_number,
          "CurrentBlockTime":current_block,
          "NextBlockTime":next_block,
          "TimeElapsed":time_elapsed,
          "TimeRemaining":time_remaining
           })
class SampleApi(APIView):
    """Test API View"""
    def get(self, request, format=None):
        """Returns a list of api view features"""
        return Response({
                "$id": "1",
                 "ContentEncoding": null,
                 "ContentType": null,
                "JsonRequestBehavior": 1,
                "Max3sonLength": null,
                "RecursionLimitn": null})

class GetDesisionAspectCumBlock_New(APIView):
    """Test API View"""
    def get(self, request, format=None):
        """Returns a list of api view features"""
        return Response({
                "$id": "1",
                 "ContentEncoding": null,
                 "ContentType": null,
                  "Data": {"$id": "2",
                           "result": {"curblkfuelcostdcsg": 280,
                                      "expdcperc": 73.30215,
                                      "posblk": 0,
                                      "negblk": 40,
                                      "bekfreq": 49.99,
                                      "avg_hz": 0,
                                      "posb1kRate": 0,
                                      "negb1kRate": 0,
                                      "avg": null}
                         },
                "JsonRequestBehavior": 1,
                "Max3sonLength": null,
                "RecursionLimitn": null})

class GetInstanceDataRABT(APIView):
    def get(self, request, format=None):
        """Returns a list of api view features"""
        return Response({
        "$id": "1",
        "ContentEncoding": null,
        "ContentType": null,
        "Data": {
                  "$id": "2",
                  "result": {
                            "lasttwoblockdata": [{
                                                 "$id": "3",
                                                 "blockno": "54",
                                                 "blocktime": "13:15-13:30",
                                                 "dam": 562.47677800,
                                                 "sgm": 326.58792511,
                                                 "netexbusm": 285.225,
                                                 "avghz": 50.064,
                                                 "hz": 50.063,
                                                 "m": 288652.39,
                                                 "expdcperc": 50.708760104581597500190487860,
                                                 "expscperc": 87.33482718441953727993418893,
                                                 "bac kingdown": 235.88885289,
                                                 "devm": -41.36292511,
                                                 "devrate": 0.00000000,
                                                 "fuelrate": 2.80000000,
                                                 "devrs": 0.0000000000000000,
                                                 "addidevrs": 0.0,
                                                 "totaldevrs": 0.0000000000000000,
                                                 "fuelcost": 28954.0475770000000000,
                                                 "ne tgainloss": 28954.0475770000000000,
                                                 "breakFrq": 49.01000000,
                                                 "NewMeterIds": [2, 4],
                                                 "CurrentTime": "2020-07-19T18:19:33.4539655+05:30"},
                                                 {
                                                 "$id ": "4",
                                                 "blockno ": "53",
                                                 "blocktime ": "13: 00 - 13: 15",
                                                 "dcm": 562.47677800,
                                                 "sgme": 326.58792511,
                                                 "netexbusm": 283.162,
                                                 "avghz": 50.052,
                                                 "hz": 50.05207,
                                                 "me": 288652.39,
                                                 "expdcperc ": 50.341989407427589837317692780,
                                                 "expscperc ": 86.70314430780823916297913860,
                                                 "b ackingdown ": 235.88885289,
                                                 "devmw ": -43.42592511,
                                                 "devrate ": 0.00000000,
                                                 "fuelrate ": 2.80000000,
                                                 "devrs ": 0.0,
                                                 "addidevrs ": 0.0,
                                                 "totaldevrs ": 0.0,
                                                 "fuelcost ": 30398.1475770000000000,
                                                 "netgainloss": 30398.1475770000000000,
                                                 "breakFrq": 49.01000000,
                                                 "NewMeterIds ": [2, 4],
                                                 "CurrentTime ": "2020 - 07 - 19718: 19: 33.4539655 + 05: 30 "}],
			                "forlOesg": 345.20200881999273027076102674,
                            "limopoverinj": 374.58792511,
                            "limopunderinj": 278.58792511,
                            "askrateoverinj": 414.80289936880070486703660633,
                            "askrateun derinj": 275.60111827118475567448544715,
                            "overinjopplAk": 0.0,
                            "underinjoppblk": 3.14998274463421625271294806,
                            "cumexpdcperc": 93.39003634155405866816985510,
                            "posblk": 0,
                            "negblk": 17,
                            "acp": 240.86800000,
                            "countv ": 6,
                            "posblkAbove20Mw": 0,
                            "negblkAbove2OW": 0,
                            "NoOfVoilence_pos ": 0,
                            "NoOfVoilence_neg ": 0,
                            "ecr ": 240.8680000011,
                            "JsonRequestBehavior ": 1,
                            "Max3sonLength": null,
                            "RecursionLimie": 0
                            }
	           }
        })

class GetNextFourBlocks_Final(APIView):
    def get(self, request, format=None):
        """Returns a list of api view features"""
        return Response({"$id": "1",
                         "ContentEncoding": null,
                         "ContentTypen": null,
                         "Data ": {"$id ": "2",
                                   "result ": [{"$id": "3",
                                                "blockno ": 55,
                                                "dcvalue ": 562.47677800,
                                                "sgvalue ": 326.58792511,
                                                "ftfhz ": 49.98275,
                                                "blocktime": 0},
                                               {"$ref": "3"},
                                               {"$ref": "3 "},
                                               {"$ref": "3 "},
                                               {"$ref": "3 "},
                                               {"$ref": "3"},
                                               {"$ref": "3 "},
                                               {"$id ": "4 ",
                                                "blockno ": 56,
                                                "dcvalue ": 562.47677800,
                                                "sgvalue ": 326.58792511,
                                                "ftfhz ": 49.9768125,
                                                "blocktime": null},
                                               {"$ref ": "4 "},
                                               {"$ref ": "4 "},
                                               {"$ref ": "4 "},
                                               {"$ref ": "4 "},
                                               {"$ref": "4"},
                                               {"Sref": "4",
                                                "Sid": "5",
                                                "blockno": 57,
                                                "dcvalue": 562.47677800,
                                                "sgvalue": 326.58792511,
                                                "ftfhz": 49.9815625,
                                                "blocktime": null},
                                               {"$ref": "5"},
                                               {"$ref": "5"},
                                               {"$ref": "5"},
                                               {"$ref": "5"},
                                               {"$ref": "5"},
                                               {"$ref ": "5 "},
                                               {"$id ": "6 ",
                                                "blockno ": 58,
                                                "dcvalue ": 562.47677800,
                                                "sgvalue ": 326.58792511,
                                                "ftfhz ": 49.9455,
                                                "blocktime": null},
                                               {"$ref": "6"},
                                               {"$ref": "6"},
                                               {"$ref": "6"},
                                               {"$ref": "6"},
                                               {"$ref": "6"},
                                               {"$ref": "6"}]},
	               "JsonRequestBehavior": 0,
	               "MaxJsonlength": 0,
	               "RecursionLimie": null})

class GetNextFourBlocks_Final(APIView):
    def get(self, request, format=None):
        """Returns a list of api view features"""
        return Response({
        	"$id": "1",
	        "ContentEncoding": null,
	        "ContentTypen": null,
	        "Data ": {
		    "$id ": "2",
		    "result ": [{
				"$id": "3",
				"blockno ": 55,
				"dcvalue ": 562.47677800,
				"sgvalue ": 326.58792511,
				"ftfhz ": 49.98275,
				"blocktime": 0
			},
			{
				"$ref": "3"
			},
			{
				"$ref": "3 "
			}, {
				"$ref": "3 "
			}, {
				"$ref": "3 "
			}, {
				"$ref": "3"
			},
			{
				"$ref": "3 "
			},
			{
				"$id ": "4 ",
				"blockno ": 56,
				"dcvalue ": 562.47677800,
				"sgvalue ": 326.58792511,
				"ftfhz ": 49.9768125,
				"blocktime": null
			},
			{
				"$ref ": "4 "
			},
			{
				"$ref ": "4 "
			},
			{
				"$ref ": "4 "
			},
			{
				"$ref ": "4 "
			},
			{
				"$ref": "4"
			},
			{
				"Sref": "4",
				"Sid": "5",
				"blockno": 57,
				"dcvalue": 562.47677800,
				"sgvalue": 326.58792511,
				"ftfhz": 49.9815625,
				"blocktime": null
			},
			{
				"$ref": "5"
			},
			{
				"$ref": "5"
			},
			{
				"$ref": "5"
			},
			{
				"$ref ": "5"
			},
			{
				"$ref": "5"
			},
			{
				"$ref ": "5 "
			}, {
				"$id ": "6 ",
				"blockno ": 58,
				"dcvalue ": 562.47677800,
				"sgvalue ": 326.58792511,
				"ftfhz ": 49.9455,
				"blocktime": null
			}, {
				"$ref ": "6 "
			},
			{
				"$ref": "6"
			},
			{
				"$ref": "6"
			},
			{
				"$ref": "6"
			},
			{
				"$ref ": "6 "
			},
			{
				"$ref": "6"
			}
		    ]
	        },
	        "JsonRequestBehavior": 0,
	        "MaxJsonlength": 0,
	        "RecursionLimie": null
            })

class GetDCSGLastBlockData_New(APIView):
    def get(self, request, format=None):
        """Returns a list of api view features"""
        return Response({"$id": "1",
	    "ContentEncoding": null,
	    "ContentType": null,
	    "Data": {
		"$id": "2",
		"resule": {
			"dtdate ": "20 / 07 / 2020 ",
			"dttime ": "13: 21: 45 ",
			"dcvalue ": 6876.21543800,
			"sgvalue ": 5324.481009745,
			"backingdown ": 1551.734428255,
			"export ": 4972.53475,
			"import ": 0.0,
			"netexp ": 4972.53475,
			"underinjectionmwh": -363.128319745,
			"noverinjectionmwh ": 11.18206000,
			"underinjectionlacs": -5.2145523602144986,
			"Koverinjectionlacs ": 0.1725586535200000,
			"devmwh ": -351.946259745,
			"devmhlacs ": -5.0419937066944986,
			"addidev ": 0.0,
			"totald ev ": -5.0419937066944986,
			"fuelcose": -9.8544952728600000,
			"netgainloss": -14.8964889795544986,
			"uipayablemonth": 0.0,
			"uireceivablemonth": 0.0,
			"netuimonth": 0.0,
			"netgainlossmonth": 0.0,
			"ListDevMWData": [-51.86076000, -15.06376000, -51.39376000, -56.57176000, -31.44776000, -15.94392511, -35.38292511, -7.91356907, -6.87571108, -6.41592511, -54.35676000, -27.03776000, -33.40976000, -0.22485310, -38.81992511, -53.63776000, -45.53776000, -20.37792511, -40.22192511, -25.59876000, -10.57176000, -11.66276000, -6.79300000, -10.19692511, -53.57976000, -5.97076000, -51.58576000, -34.11176000, -10.16085310, -35.05592511, -37.74392511, -43.42592511, -48.13276000, -9.98276000, -15.20592511, -53.84876000, -46.21976000, -43.95676000, -34.83776000, -15.17676000, 41.96400000, -16.17976000, -18.40676000, -26.14985310, -9.26976000, -8.43076000, -5.83776000, 2.76424000, -27.32285310, -51.06776000, -17.91976000, -35.78692511, -39.82792511],
			"PosCount": 2.0,
			"NegCount": 51.0,
			"addidevrsViolation": 0.0,
			"ListAvvw": null,
			"ListSG": null,
			"ListBlockli": null,
			"ListUIRate ": null,
			"GenExport ": 0.0,
			"APC ": 0.0,
			"APCPer ": 0.0,
			"kw ": 0.0,
			"RSEnergyLoss_Frequency ": 0.0,
			"KWEnergyLoss_Frequency ": 0.0,
			"SumData ": null,
			"DataValue ": null,
			"JsonRequestBehavior ": 1,
			"MaxJsonLength ": null,
			"RecursionLimie": null
		        }
	        }
        })

class GetInstanceDataRABT_CurrentBlockNX4_Final(APIView):
    def get(self, request, format=None):
        """Returns a list of api view features"""
        return Response({
        "Vid": "1",
	"ContentEncoding": null,
	"ContentType": null,
	"Data": {
		"$id": "2",
		"result": {
			"lasttwoblockdata": [{
				"$id": "3",
				"blockno": "55",
				"blocktime": "13:30 - 13:45",
				"dcm": 562.47677800,
				"sgm": 326.58792511,
				"netexbusm": 278.218,
				"avghz": 50.095,
				"hz": 50.077,
				"me": 278466.109,
				"expdcperc ": 49.463019787103104192507659400,
				"expscperc ": 85.18931001698601042317023464,
				"ba ckingdown ": 235.88885289,
				"devm ": -48.36992511,
				"devrate ": 0.00000000,
				"fuelrate ": 2.80000000,
				"devrs ": 0.0,
				"addidevrs ": 0.0,
				"totaldevrs ": 0.0,
				"fuelcost ": 33858.9475770000000000,
				"netgainloss ": 33858.9475770000000000,
				"breakFrq": 49.01000000,
				"NewMeterIds ": [2, 4],
				"CurrentTime ": "2020 - 07 - 19 T18: 35: 43.0001211 + 05: 30 ",
				"shift ": null},
                {
				"$id": "4",
				"blockno": "54",
				"blocktime": "13:15 - 13:30",
				"dcm": 562.47677800,
				"sgm": 326.58792511,
				"netexbusm": 283.343,
				"avghz": 50.08,
				"hz": 50.0832,
				"m": 278466.109,
				"expdcperc": 50.374168513673288037501878880,
				"expscperc": 86.75856583018664195462667331,
				"ba ckingdown": 235.88885289,
				"devm": -43.24492511,
				"devrate": 0.00000000,
				"fuelrate": 2.80000000,
				"devrs": 0.0,
				"addidevrs": 0.0,
				"totaldevrs": 0.0,
				"fuelcost": 30271.4475770000000000,
				"netgainloss": 30271.4475770000000000,
				"breakFrq": 49.01000000,
				"NewMeterIds": [2, 4],
				"CurrentTime": "2020-07- 19T18:35:43.0001211+05:30",
				"shife": null}],
			"for100sg ": 359.03390617493159076477314996,
			"limopoverinj ": 374.58792511,
			"filimopunderinj": 278.58792511,
			"askrateoverinj": 439.2317457947977368984261404,
			"askrateund erinj": 278.83606655506544463112015952,
			"overinjoppblk": 0.0,
			"nunderinjoppblk ": 15.33679107554000126046870273,
			"cumexpdcperc ": 93.28988341332464350513380132,
			"posblk ": 0,
			"negblk ": 18,
			"acp ": 240.8800000,
			"countv ": 6,
			"posblkAbove20Mw ": 0,
			"negblkAbove20Mw ": 0,
			"NoOfVoilence_pos ": 0,
			"NoOfVoilence_neg ": 0,
			"ecr ": 240.8680000011,
			"JsonRequestBehavior ": 1,
			"MaxJsonLength ": null,
			"RecursionLimie": null}
	      }
        })



class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.UserProfileSerializer
    queryset=models.UserProfile.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permissions.UpdateOwnProfile,)

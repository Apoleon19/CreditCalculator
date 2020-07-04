import argparse
from math import log, ceil, floor


def get_interest_rate(percent):
    return percent / 12 / 100


def calculate_count_of_month(principal, monthly_payment, credit_interest):
    rate = get_interest_rate(credit_interest)

    annuity_payment = log(monthly_payment / (monthly_payment - rate * principal), 1 + rate)
    count_of_months = ceil(annuity_payment)

    years = f'You need {count_of_months // 12} years'
    months = f' and {count_of_months % 12} months'
    replay = ' to repay this credit!'

    print(years + months + replay) if count_of_months % 12 else print(years + replay)
    overpayment = count_of_months * monthly_payment - principal
    print(f'Overpayment = {overpayment}')


def calculate_annuity_payment(principal, periods, credit_interest):
    rate = get_interest_rate(credit_interest)
    numerator = rate * pow(1 + rate, periods)
    denominator = pow(1 + rate, periods) - 1
    annuity_payment = ceil(principal * (numerator / denominator))

    print(f'Your annuity payment = {annuity_payment}!')
    overpayment = periods * annuity_payment - principal
    print(f'Overpayment = {overpayment}')


def calculate_credit_principal(payment, periods, credit_interest):
    rate = get_interest_rate(credit_interest)

    numerator = rate * pow(1 + rate, periods)
    denominator = pow(1 + rate, periods) - 1
    credit_principal = floor(payment / (numerator / denominator))

    print(f'Your credit principal = {credit_principal}!')
    print(f'Overpayment = {payment * periods - credit_principal}')


def calculate_differentiated_payments(principal, credit_interest, periods):
    rate = get_interest_rate(credit_interest)

    def get_month_payment(month: int):
        return ceil(principal / periods + rate * (principal - principal * (month - 1) / periods))

    all_months_payment = 0
    for period in range(periods):
        current_month_payment = get_month_payment(period + 1)
        all_months_payment += current_month_payment
        print(f'Month {period + 1}: paid out {current_month_payment}')

    overpayment = all_months_payment - principal
    print(f'\nOverpayment = {overpayment}')


def console_mode():
    parser = argparse.ArgumentParser(description='Credit calculator')
    parser.add_argument('--type', type=str)

    group = parser.add_argument_group()
    group.add_argument('--interest', type=float)
    group.add_argument('--payment', type=int)
    group.add_argument('--periods', type=int)
    group.add_argument('--principal', type=int)

    args, argv = parser.parse_known_args()

    is_diff = bool(args.principal and args.periods and args.interest and args.type == "diff")
    is_annuity = bool(args.principal and args.periods and args.interest and args.type == "annuity")
    is_principal = bool(args.payment and args.periods and args.interest and args.type == "annuity")
    is_repay_time = bool(args.principal and args.payment and args.interest and args.type == "annuity")

    if not argv and bool(is_diff or is_principal or is_repay_time or is_annuity):
        if is_diff:
            calculate_differentiated_payments(args.principal, args.interest, args.periods)
        elif is_annuity:
            calculate_annuity_payment(args.principal, args.periods, args.interest)
        elif is_principal:
            calculate_credit_principal(args.payment, args.periods, args.interest)
        else:
            calculate_count_of_month(args.principal, args.payment, args.interest)
    else:
        print('Incorrect parameters')


def main():
    calc_type = input('What do you want to calculate?\n'
                      'type "n" - for count of months,\n'
                      'type "a" - for annuity monthly payment,\n'
                      'type "p" - for credit principal:\n> ')

    credit_principal_str = 'Enter credit principal:\n> '
    monthly_payment_str = 'Enter monthly payment:\n> '
    credit_interest_str = 'Enter credit interest:\n> '
    periods_str = 'Enter count of periods:\n> '

    if calc_type == 'n':
        credit_principal = int(input(credit_principal_str))
        monthly_payment = int(input(monthly_payment_str))
        credit_interest = float(input(credit_interest_str))
        calculate_count_of_month(credit_principal, monthly_payment, credit_interest)
    elif calc_type == 'a':
        credit_principal = int(input(credit_principal_str))
        periods = int(input(periods_str))
        credit_interest = float(input(credit_interest_str))
        calculate_annuity_payment(credit_principal, periods, credit_interest)
    elif calc_type == 'p':
        monthly_payment = float(input(monthly_payment_str))
        periods = int(input(periods_str))
        credit_interest = float(input(credit_interest_str))
        calculate_credit_principal(monthly_payment, periods, credit_interest)


if __name__ == '__main__':
    # main()
    console_mode()

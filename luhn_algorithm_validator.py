def credit_card():
    card_number=input('what is your credit card number?')
    only_numbers=''.join(chars for chars in card_number if chars.isdigit())
    return only_numbers   
def add_odd(just_numbers):
    reverse_numbers=just_numbers[::-1]
    sum_odd=0
    for numbers in reverse_numbers[::2]:
            sum_odd+=int(numbers)
    return sum_odd
def add_even(even_numbers):
    reversed_even_number=even_numbers[::-1]
    sum_even=0
    for numbers1 in reversed_even_number[1::2]:
        numbers1=int(numbers1)*2
        if int(numbers1) < 10:
            sum_even+=int(numbers1)
        else:
            suming=int(numbers1)//10 + int(numbers1)%10
            sum_even+=suming
    return sum_even
value=credit_card()
Final_value=add_odd(value)+add_even(value)
if Final_value % 10 == 0:
    print('valid') 
else:
    print('not valid')  

        
        
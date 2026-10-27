def banner(title):
    print('='*40)
    print(' '*12,title.upper())
    print('='*40)
def basic_info(message):
    print(f'length:{len(message)}')
    print(f'first:{message[0]}')
    print(f'last:{message[-1]}')
def format_username(username):
        print(f'{username[0:3]}...{username[-2]}{username[-1]}({username[::-1]})')
def contains_banned(message,banned_word):
    print(banned_word in message)
def censor_message(message,banned_word):
    if banned_word.lower() in message.lower():
        message=message.replace(banned_word,'***')
        print(message)
    else:
        print(message)
def word_stats(message,target_word):
    print(f'words:{len(message.split())}')
    print(f'{target_word.lower()} appears {message.lower().split().count(target_word)} times')
def main():
    banner('chat analyzer')
    message=input('Enter your user message please')
    username=input('Enter username')
    basic_info(message)
    format_username(username)
    banned_word=input('Do you have any banned words')
    contains_banned(message,banned_word)
    censor_message(message,banned_word)
    target_word=input('Do you have any target words?')
    word_stats(message,target_word)
    print('This is end')
main()
    
    

    


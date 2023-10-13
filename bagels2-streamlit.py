# bagels2-streamlit.py
# run via terminal> streamlit run bagels2-streamlit.py

import random
import streamlit as st

NUM_DIGITS: int = 3  # does not change per session
MAX_GUESS: int = 10  # does not change, but used to seed guesses left session state

def init_page():
    # Initialize page
    st.set_page_config(
        page_title="Bagels Game",
        page_icon=":bagel:",
        layout="wide"
    )
    # setup initial display text at top
    st.header(' :bagel: The Bagels Game :bagel:')
    st.markdown('<style>div.block-container{padding-top:2rem;}</style>',
        unsafe_allow_html=True
    )
    # setup columns
    text_column, rule_column = st.columns((2,2))
    # setup column text
    with text_column:
        # setup rules of the game and display text
        st.markdown('#')
        st.subheader(f'I will think of a {NUM_DIGITS}-digit number.')
        st.subheader('_Each digit is unique._')
        st.subheader(f'You will try to guess what it is in {MAX_GUESS} guesses or less.')
        st.markdown('#')
    with rule_column:
        st.write(":bagel:"*20)
        # You can use markdown in st.write commands
        st.write(
            """
            The clues I give (one or more depending on situation) are... 
            | **When I say** | **That means**                                 |
            |-----------------|-------------------------------------------------|
            | _Bagels_        | None of the digits are correct.                 |
            | _Pico_          | One digit is correct but in the wrong position. |
            | _Fermi_         | One digit is correct and in the right position. |
            """
        )
        st.write(":bagel:"*20)
    return text_column

def init_session(text_column):
    # Initialize system state or clear it
    with text_column:
        play_again = st.button(label="Re-start / Play Again", use_container_width=False)
    if play_again or "messages" not in st.session_state:
        # re-run by simple reset of all session state info
        # delete all the items in Session state
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.messages = [] # must set this again here or error
    return

def getSecretNum():
    # Returns a string of unique random digits that is NUM_DIGITS long.
    numbers = list(range(10))
    random.shuffle(numbers)
    secretNum = ''
    for i in range(NUM_DIGITS):
        secretNum += str(numbers[i])
    return secretNum

def getClues(guess, secretNum):
    # Returns a string with the Pico, Fermi, and Bagels clues to the user.
    if guess == secretNum:
        return 'You got it!'    
    clues = []
    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            clues.append('Fermi')
        elif guess[i] in secretNum:
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'    
    clues.sort()
    return ' '.join(clues)

def isOnlyDigits(num):
    # Returns True if num is a string of only digits. Otherwise returns False.
    if num == '':
        return False
    for i in num:
        if i not in '0 1 2 3 4 5 6 7 8 9'.split():
            return False  
    return True

def main():
    # Main program
    text_column = init_page()
    init_session(text_column)
    st.write("---")  # divider

    # Initialize session and chat history, using 2 different notations for fun
    # every input re-runs the entire page so need session state info to carry over
    if 'guessesLeft' not in st.session_state:
        st.session_state['guessesLeft'] = MAX_GUESS
        response = f'I have thought up a number. You have {st.session_state.guessesLeft} guesses to get it.'
        # Add assistant response to chat history but don't show it on first run yet
        st.session_state.messages.append({"role": "assistant", "content": response})

    # get ready to play by grabbing secret number
    if 'secretNum' not in st.session_state:
        st.session_state['secretNum'] = getSecretNum()

    # display chat messages from history on app rerun, avatar="🥯"
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="🥯"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar="🦖"):
                st.markdown(message["content"])

    # react to user input
    if guess := st.chat_input('Guess', max_chars=NUM_DIGITS):
        # user took a guess
        # check if valid before counting it
        if isOnlyDigits(guess):
            st.session_state.guessesLeft -= 1
            
            # display user message in chat container
            response = f'Guess #{int(10) - st.session_state.guessesLeft} --> ' + guess
            st.chat_message("user", avatar="🦖").write(response)
            
            # Add user response to chat history
            st.session_state.messages.append({"role": "user", "content": response})
            
            # get clue/hint for that guess + display assistant message in chat container
            clue = getClues(guess, st.session_state.secretNum)
            if clue == 'You got it!':
                st.chat_input(disabled=True) # game is done
            response = f'Clue #{int(10) - st.session_state.guessesLeft} --> ' + clue
            st.chat_message("assistant", avatar="🥯").write(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Check if out of guesses st.session_state.guessesLeft == 0
            if st.session_state.guessesLeft == 0:
                response = 'GAME OVER'
                st.chat_message("assistant", avatar="🥯").write(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.chat_input(disabled=True)
        else:  # show message and ignore until next input
            st.chat_message("user", avatar="🦖").write('Must be numbers only!! >>>Guess again<<<')  
    return

if __name__ == "__main__":
    main()  
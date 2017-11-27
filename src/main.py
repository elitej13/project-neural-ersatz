import sympy as sy
import tensorflow as tf
import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from random import randint



class Main(BoxLayout):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.menu = Menu(self, orientation='vertical')
        self.add_widget(self.menu)

    def switchToRSAScreen(self, priorScreen):
        self.remove_widget(priorScreen)
        self.rsa = RSAScreen(self, orientation='vertical')
        self.add_widget(self.rsa)

    def switchToHillScreen(self, priorScreen):
        self.remove_widget(priorScreen)
        self.hill = HillScreen(self, orientation='vertical')
        self.add_widget(self.hill)


class Menu(BoxLayout):
    def __init__(self, main, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.main = main

        self.title = Label(text='Choose an Encryption Scheme')
        self.rsa = Button(text='RSA')
        self.hill = Button(text='Hill Cipher')

        self.add_widget(self.title)
        self.add_widget(self.rsa)
        self.add_widget(self.hill)

        def rsa_click(instance):
            self.main.switchToRSAScreen(self)
        def hill_click(instance):
            self.main.switchToHillScreen(self)

        self.rsa.bind(on_press=rsa_click)
        self.hill.bind(on_press=hill_click)




class RSAScreen(BoxLayout):
    def __init__(self, main, **kwargs):
        super(RSAScreen, self).__init__(**kwargs)

        self.first_screen = BoxLayout(orientation='vertical')
        self.second_screen = BoxLayout(orientation='vertical')
#------------------------First Screen----------------------------#
        self.title = Label(text="RSA Encryption")

        self.p = BoxLayout(orientation='horizontal')
        self.p_label = Label(text='Choose a number')
        self.p_input = TextInput(multiline=False)
        self.p.add_widget(self.p_label)
        self.p.add_widget(self.p_input)
        self.p_result = Label()

        self.q = BoxLayout(orientation='horizontal')
        self.q_label = Label(text='Choose a number')
        self.q_input = TextInput(multiline=False)
        self.q.add_widget(self.q_label)
        self.q.add_widget(self.q_input)
        self.q_result = Label()

        self.confirm = Button(text="Confirm Choices")

        self.p_was_chosen = False
        self.q_was_chosen = False

        self.first_screen.add_widget(self.title)
        self.first_screen.add_widget(self.p)
        self.first_screen.add_widget(self.p_result)
        self.first_screen.add_widget(self.q)
        self.first_screen.add_widget(self.q_result)
        self.first_screen.add_widget(self.confirm)

        self.add_widget(self.first_screen)

        def p_validate(instance):
            p = int(self.p_input.text)
            self.p_choice = sy.nextprime(p)
            self.p_result.text = "The next prime found was " + str(self.p_choice)
            self.p_was_chosen = True
        def q_validate(instance):
            q = int(self.q_input.text)
            self.q_choice = sy.nextprime(q)
            self.q_result.text = "The next prime found was " + str(self.q_choice)
            self.q_was_chosen = True
        def confirm(instance):
            if(self.p_was_chosen & self.q_was_chosen):
                self.init_second_screen()

        self.p_input.bind(on_text_validate=p_validate)
        self.q_input.bind(on_text_validate=q_validate)
        self.confirm.bind(on_press=confirm)

#------------------------Second Screen----------------------------#

        self.key_pub = Label()
        self.key_pri = Label()
        self.second_screen.add_widget(self.key_pub)
        self.second_screen.add_widget(self.key_pri)

    def init_second_screen(self):
        self.remove_widget(self.first_screen)
        p = self.p_choice
        q = self.q_choice
        n = p * q
        phi = (p - 1) * (q - 1)
        e = sy.nextprime(int(n / 2))
        d = sy.invert(e, phi)

        self.key_pub.text = "Public key: (" + str(e) + ", " + str(n) + ")"
        self.key_pri.text = "Private key: (" + str(d) + ", " + str(n) + ")"

        self.add_widget(self.second_screen)



class HillScreen(BoxLayout):
    def __init__(self, main, **kwargs):
        super(HillScreen, self).__init__(**kwargs)

        self.encrpytion_screen = BoxLayout(orientation='vertical')
        self.instruction = Label(text="Enter a message to be encrypted then press enter to generate posible block sizes.")
        self.message = TextInput(multiline=False)

        self.cont = BoxLayout(orientation='horizontal')
        self.blocksize = Button(text="Block Size")
        self.generate = Button(text="Generate Matrices")
        self.cont.add_widget(self.blocksize)
        self.cont.add_widget(self.generate)

        self.matrices_message = Label()

        self.encrpytion_screen.add_widget(self.instruction)
        self.encrpytion_screen.add_widget(self.message)
        self.encrpytion_screen.add_widget(self.cont)
        self.encrpytion_screen.add_widget(self.matrices_message)

        self.add_widget(self.encrpytion_screen)


        def is_number(n):
            try:
                int(n)
                return True
            except ValueError:
                return False

        def message_validate(instance):
            m = self.message.text
            l = len(m)
            while(sy.isprime(l)):
                m += " "
                l = len(m)
            b = sy.divisors(l)
            self.dropdown = DropDown();
            for i in range(len(b) - 2):
                btn = Button(text=str(b[i + 1]), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(btn)
            self.blocksize.bind(on_release=self.dropdown.open)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self.blocksize, 'text', x))

        def generate_matrices(instance):
            n = self.blocksize.text
            if(is_number(n)):
                n = int(n)
                key = sy.zeros(n, n)
                for i in range(n):
                    for j in range(n):
                        r = randint(0, 29)
                        print(r)
                        key[i, j] = r

                print(key)



        self.message.bind(on_text_validate=message_validate)
        self.generate.bind(on_press=generate_matrices)







class Runtime(App):

    def build(self):
        return Main()


if __name__ == '__main__':
    Runtime().run()

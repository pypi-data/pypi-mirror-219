import PySimpleGUI as sg


class EventSimpleGUI:

    """ Use this class to start a window and create events  """

    def __init__(self):
        """ self._events holds all events """
        self._events = []

    @property
    def get_events(self) -> list:
        """ Use this property to get all events, from @event or add_event """
        return self._events

    def add_event(self, event):
        """ You can use this method, but it's recomended to use @EventSimpleGUI.event """
        self._events.append(event)

    def run_window(
            self, Window: sg.Window, *args, window_log=False, close_event=False, return_values=True, task=None
    ) -> dict or None:
        """ Use this method to run PySimpleGUI Windows
        :param Window:         can be any PySimpleGUI Window
        :type Window:          PySimpleGUI.Window
        :arg args:             can be any function that recives (event: str , values: dict, window: PySimpleGUI.Window)
        :type args:            function
        :param window_log:     if True prints events and values on the console
        :type window_log:      bool
        :param return_values:  if True return values of window.read()
        :type return_values:   bool
        :param task:           can be any callable function
        :param close_event:    a diferent key to close the window
        """
        while True:

            event, values = Window.Read()

            # Run task
            if task:
                task()

            # Run decorator events
            for func in self._events:
                func(event, values, Window)

            # Run args events or functions
            for arg in args:
                arg(event, values, Window)

            # Enable log
            if window_log:
                print(f'{"Event ->":10}', event)
                print(f'{"Values ->":10}', values)

            # Close window
            if event == sg.WIN_CLOSED or event == close_event:
                break

            # return window on the values
            values['Window'] = Window

        # Return values of window.read()
        Window.close()

        if return_values:
            return values

    def event(self, key: str or list[str]):
        """ Use this decorator to create events.
        ::param key:     element key or list of element keys
        ::type key:      str or list[str]

        Exemple of a simple event:

        app = EventSimpleGUI()
        @app.event('_CLICK_')
        def print_when_click(event: str , values: dict, window: PySimpleGUI.Window):
            print('click!')

        * All events will recive (event: str , values: dict, window: PySimpleGUI.Window)
        """
        def decorador(func_event):
            def empacotador(event: str, values: dict, window: sg.Window):
                if type(key) == list:
                    if event in key:
                        window.write_event_value(f'{func_event.__name__}', func_event(event, values, window))
                        
                elif type(key) == str:
                    if event == key:
                        window.write_event_value(f'{func_event.__name__}', func_event(event, values, window))

            self.add_event(empacotador)
            return empacotador
        return decorador








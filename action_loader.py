#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import imp
import os
import logging
import collections

logger = logging.getLogger(__name__)


class ActionLoader(object):

    def __init__(self, main_module='__init__'):
        self.actions_folder = 'actions'
        self.main_module = main_module
        self.loaded_action_modules = collections.OrderedDict({})

    def get_available_action_modules(self):
        """
        Returns a dictionary of action modules available in actions directory
        """
        action_modules = {}
        for possible_module in os.listdir(self.actions_folder):
            location = os.path.join(self.actions_folder, possible_module)
            if os.path.isdir(location) and self.main_module + '.py' in os.listdir(location):
                info = imp.find_module(self.main_module, [location])
                action_modules[possible_module] = {
                    'name': possible_module,
                    'info': info
                }
        return action_modules

    def get_loaded_action_modules(self):
        """
        Returns a dictionary of the loaded action modules
        """
        return self.loaded_action_modules.copy()

    def load_action_module(self, module_name):
        """
        Loads action module
        """
        action_modules = self.get_available_action_modules()
        if module_name in action_modules:
            if module_name not in self.loaded_action_modules:
                module = imp.load_module(self.main_module, *action_modules[module_name]['info'])
                self.loaded_action_modules[module_name] = {
                    'name': module_name,
                    'info': action_modules[module_name]['info'],
                    'module': module
                }
                logger.info('action module "%s" loaded' % module_name)
            else:
                logger.warning('action module "%s" already loaded' % module_name)
        else:
            logger.error('cannot locate action module "%s"' % module_name)
            raise Exception('cannot locate action module "%s"' % module_name)

    def unload_action_module(self, action_name):
        """
        Unloads an action module
        """
        del self.loaded_action_modules[action_name]
        logger.info('action "%s" unloaded' % action_name)

    def execute_action(self, module, action_name, entities, context):
        """
        Executes action functions contained in the loaded action modules.
        """
        action_info = self.loaded_action_modules.get(module)
        module = action_info['module']
        if hasattr(module, action_name):
            action = getattr(module, action_name)
            context['LAST_RESULT'] = result = action(entities, context)
            return result

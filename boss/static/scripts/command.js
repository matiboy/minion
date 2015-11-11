angular.module('Boss', ['ui.bootstrap'])
    .controller('CommandController', function($scope, $http) {
        $scope.obj = window.command;
        // Default channels
        if(!window.editing) {
            $scope.obj.channel = 'minion:command';
            $scope.obj.action = 'minion:do';
        }
        $scope.availableCommandClasses = _.pluck(window.availableCommands, 'class');
        // Check current one in same loop
        var currentSystems = {};
        _.each(window.availableCommands, function(command) {
            if(command.class === $scope.obj.class) {
                command.configuration = $scope.obj.configuration;
            } else {
                command.configuration = _.zipObject(_.pluck(command.setup, 'name'),_.pluck(command.setup, 'default'));
            }
            currentSystems[command.class] = command;
        });
        $scope.systems = currentSystems;

        $scope.submit = function() {
            $scope.obj.configuration = currentSystems[$scope.obj.class].configuration;
            var obj = angular.copy($scope.obj);
            if(obj.channel) {
                obj.configuration.channel = obj.channel;
                delete obj.channel;
            }
            if(obj.action) {
                obj.configuration.action = obj.action;
                delete obj.action;
            }
            obj.configuration.expressions = obj.expressions.split('\n')
            delete obj.expressions;
            $http.post('/save_object/commands', obj)
                .then(function(resp){
                    window.alert('Command saved successfully');
                })
                .finally(console.debug.bind(console));
        };
    });

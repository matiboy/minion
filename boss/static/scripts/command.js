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
            if($scope.obj.channel) {
                $scope.obj.configuration.channel = $scope.obj.channel;
                delete $scope.obj.channel;
            }
            if($scope.obj.action) {
                $scope.obj.configuration.action = $scope.obj.action;
                delete $scope.obj.action;
            }
            $http.post('/save_object/commands', $scope.obj)
                .then(function(resp){
                    window.alert('Command saved successfully');
                })
                .finally(console.debug.bind(console));
        };
    });

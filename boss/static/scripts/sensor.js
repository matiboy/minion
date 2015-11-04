angular.module('Boss', ['ui.bootstrap'])
    .controller('SensorController', function($scope, $http) {
        $scope.obj = window.sensor;
        $scope.availableSensorClasses = _.pluck(window.availableSensors, 'class');
        // Check current one in same loop
        var currentSystems = {};
        _.each(window.availableSensors, function(sensor) {
            if(sensor.class === $scope.obj.class) {
                sensor.configuration = $scope.obj.configuration;
            } else {
                sensor.configuration = _.zipObject(_.pluck(sensor.setup, 'name'),_.pluck(sensor.setup, 'default'));
            }
            currentSystems[sensor.class] = sensor;
        });
        $scope.systems = currentSystems;

        $scope.submit = function() {
            $scope.obj.configuration = currentSystems[$scope.obj.class].configuration;
            _.each($scope.obj.postprocessors, function(p) {
                p.name = p.class;
            });
            $http.post('/save_object/sensors', $scope.obj)
                .then(function(resp){
                    window.alert('Sensor saved successfully');
                })
                .finally(console.debug.bind(console));
        };
    });
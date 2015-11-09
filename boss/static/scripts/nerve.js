angular.module('Boss', [])
    .controller('NervousSystemController', function($scope, $http) {
        $scope.obj = window.nerve;
        $scope.availableNerveClasses = _.pluck(window.availableNerves, 'class');
        // Check current one in same loop
        var currentSystems = {};
        _.each(window.availableNerves, function(nerve) {
            // No $scope.obj if new configuration
            if($scope.obj && nerve.class === $scope.obj.class) {
                nerve.configuration = $scope.obj.configuration;
            } else {
                nerve.configuration = _.zipObject(_.pluck(nerve.setup, 'name'),_.pluck(nerve.setup, 'default'));
            }
            currentSystems[nerve.class] = nerve;
        });
        $scope.systems = currentSystems;

        $scope.submit = function() {
            $scope.obj.configuration = currentSystems[$scope.obj.class].configuration;
            $http.post('/save_nerve', $scope.obj)
                .then(function(resp){
                    var msg = 'Nervous system saved successfully';
                    if(resp.data.installs && resp.data.installs.length) {
                      msg += '\nBigBoss is installing the following dependencies: ' + resp.data.installs.join(', ');
                    }
                    window.alert(msg);
                })
                .finally(console.debug.bind(console));
        };
    });

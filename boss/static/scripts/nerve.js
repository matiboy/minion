angular.module('Boss', [])
    .controller('NervousSystemController', function($scope, $http) {
        $scope.nerve = window.nerve;
        $scope.availableNerveClasses = _.pluck(window.availableNerves, 'class');
        // Check current one in same loop
        var currentSystems = {};
        _.each(window.availableNerves, function(nerve) {
            if(nerve.class === $scope.nerve.class) {
                nerve.configuration = $scope.nerve.configuration;
            } else {
                nerve.configuration = _.zipObject(_.pluck(nerve.setup, 'name'),_.pluck(nerve.setup, 'default'));
            }
            currentSystems[nerve.class] = nerve;
        });
        $scope.systems = currentSystems;

        $scope.submit = function() {
            $scope.nerve.configuration = currentSystems[$scope.nerve.class];
            $http.post('/save_nerve', {
                data: $scope.nerve
            }).finally(console.debug.bind(console));
        };
    });
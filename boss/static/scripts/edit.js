angular.module('Boss')
    .controller('PostprocessorsController', ['$scope', function($scope) {
        $scope.availablePostprocessClasses = _.pluck(window.availablePostprocessors, 'class');
        var pp = {};
        _.each(window.availablePostprocessors, function(p) {
            p.configuration = _.zipObject(_.pluck(p.setup, 'name'),_.pluck(p.setup, 'default'));
            pp[p.class] = p;
        });
        $scope.p = pp;

        $scope.addPostprocessor = function() {
            if(!$scope.obj.postprocessors) {
                $scope.obj.postprocessors = [];
            }
            var cp = angular.copy($scope.p[$scope.pp.class]);
            $scope.obj.postprocessors.push({configuration: cp.configuration, 'class': cp.class});
        };

        $scope.removePostprocessor = function(index){
            $scope.obj.postprocessors.splice(index, 1);
        };
    }]).controller('PreprocessorsController', ['$scope', function($scope) {
        $scope.availablePreprocessClasses = _.pluck(window.availablePreprocessors, 'class');
        var pp = {};
        _.each(window.availablePreprocessors, function(p) {
            p.configuration = _.zipObject(_.pluck(p.setup, 'name'),_.pluck(p.setup, 'default'));
            pp[p.class] = p;
        });
        $scope.p = pp;

        $scope.addPreprocessor = function() {
            if(!$scope.obj.preprocessors) {
                $scope.obj.preprocessors = [];
            }
            var cp = angular.copy($scope.p[$scope.pp.class]);
            $scope.obj.preprocessors.push({configuration: cp.configuration, 'class': cp.class});
        };

        $scope.removePreprocessor = function(index){
            $scope.obj.preprocessors.splice(index, 1);
        };
    }]);
var myApp = angular.module('myApp', ['flow','ngRoute','ui.bootstrap', 'ngSanitize']).config(['flowFactoryProvider', function (flowFactoryProvider) {
  flowFactoryProvider.defaults = {
    target: '/upload',
    permanentErrors: [404, 500, 501],
    maxChunkRetries: 1,
    chunkRetryInterval: 5000,
    simultaneousUploads: 4
  };
  flowFactoryProvider.on('catchAll', function (event) {
    //console.log('catchAll', arguments);
  });
}])
.config(['$routeProvider',function($routeProvider) {
    $routeProvider.
        when('/',{
            templateUrl: 'partials/tagSearch.html'
        }).
        when('/oriSearch', {
            controller: 'mainController',
            templateUrl: 'partials/oriSearch.html',
            resolve:{
                tags : function(tagService){
                    return tagService.getTags();
                }
            }
        }).
        otherwise({
            redirectTo: '/'
        });
        
}]);

myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        scope: false,
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

myApp.service('fileUpload', ['$http', '$q', function ($http, $q) {
    return {
        uploadFileToUrl : function(file, uploadUrl){
            var fd = new FormData();
            fd.append('file', file);
            var deferred = $q.defer();
            var promise = $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            }).success(function(response){
                deferred.resolve(response);
            }).error(function() {
                deferred.reject("upload file failed")
            });
            return deferred.promise;
        }
    }
}]);

myApp.factory('tagService', function($q){
    return {
        getTags : function(){
            data = {"tags": ["google", "apple", "culture", "design", "home", "politics", "web", "entertainment", "apps", "movie-reviews", "national-security", "policy", "gaming", "transportation", "business", "photography", "us-world", "mobile", "science", "typography", "tech", "architecture", "concepts", "microsoft"]};
            return $q.when(data['tags'])
        }
    };
});

myApp.controller('uploadCtrl', ['$scope', 'fileUpload', function($scope, fileUpload){

    $scope.$on('flow::filesSubmitted', function (event, $flow, flowFile) {
        var file = flowFile[0]['file']
        var uploadUrl = "/upload";
        fileUpload.uploadFileToUrl(file, uploadUrl).then(function(data){
            $scope.data = data;
        }, function(data){
            console.log("Upload file call back failed")
        });    
    });

    $scope.uploadFile = function(){
        var file = $scope.myFile;
        var uploadUrl = "/upload";
        fileUpload.uploadFileToUrl(file, uploadUrl).then(function(data){
            $scope.data = data;
        }, function(data){
            console.log("Upload file call back failed")
        });    
    };    
}])
.controller('mainController', function ($scope, $http, tags) {
    $scope.formData = {};
    $scope.all_tags = tags;
    $scope.search = function() {
        
    };    
});

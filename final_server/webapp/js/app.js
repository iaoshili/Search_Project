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
            templateUrl: 'partials/oriSearch.html'
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
.controller('mainController', function ($scope, $rootScope, $http, $location, $window, $timeout) {
    $scope.formData = {};

    $scope.search = function() {
        $window.location = "/?q=" + $scope.formData.query;
    };

    $scope.pageChanged = function() {
        console.log('Page changed to: ' + $scope.formData.page);
        $scope.fetchRecords();
        document.body.scrollTop = document.documentElement.scrollTop = 0;
    };

    $scope.fetchRecords = function() {
        $scope.statusText = 'Searching...';
        var start = new Date().getTime();
    var elapsed = '0.0';
    console.log("Fetching");
        $http.get('/search?q=' + escape($scope.formData.query)).success(function(data) {
            $scope.delay = (new Date().getTime() - start) / 1000.0;
            $scope.totalItems = data.numResults;
            $scope.itemsPerPage = 10; //data.itemsPerPage;
            $scope.errorText = data.error;
            $scope.statusText = '';
            var results = [];
            for (var i = 0; i < data.results.length; i++) {
                results.push("<h4><a href='" + data.results[i].url + "'>" + data.results[i].title + "</a></h4>" + data.results[i].snippet);
            }
            $scope.results = results;
            console.log("Fetched");
        })
        .error(function(data) {
            $scope.totalItems = 0;
            $scope.errorText = data;
            $scope.statusText = '';
        });
        $location.search('q', $scope.formData.query);
    };
    
    $rootScope.$on('$locationChangeSuccess', function(event){
        if ($location.search().q) {
            $scope.formData.query = $location.search().q;
            $scope.formData.page = 1;
            $scope.activeQuery = $scope.formData.query;
            $scope.fetchRecords();
        } else {
            $scope.activeQuery = false;
        }
    });
});

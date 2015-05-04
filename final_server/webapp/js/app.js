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
                "getTags" : function(){
               		data = {"tags": ["google", "apple", "culture", "design", "home", "politics", "web", "entertainment", "apps", "movie-reviews", "national-security", "policy", "gaming", "transportation", "business", "photography", "us-world", "mobile", "science", "typography", "tech", "architecture", "concepts", "microsoft"]};
		        console.log("In ng-view resolve");            
			return data['tags'];
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
}])
.service('SearchService', ['$http', '$q', function($http, $q){
    return {
        getSearchResult : function(query, tag){
            var deferred = $q.defer();
            var getUrl = '/search?q=' + query;
            if(tag){
		getUrl += '&tag=' + tag
            }
	    console.log("In SearchService getURL:" + getUrl);
            var promise = $http.get(getUrl)
	    .success(function(response){
		//console.log(response);
                deferred.resolve(response);
            }).error(function(){
                console.warn('Send to /search error');
            });
		return deferred.promise;
        }
    }
}])
;

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
.controller('mainController', function ($scope, getTags, SearchService) {
    $scope.formData = {};
    $scope.all_tags = getTags;
    $scope.search = function() {
	   query = $scope.formData.query;
	   tag = $scope.formData.search_tag;
	   console.log($scope.formData.search_tag); 
	
	   console.log($scope.formData.query); 
		console.log(SearchService);   
       SearchService.getSearchResult(query, tag).then(function(data){
        $scope.searchResult = data;
       }, function(data){
         console.log("Get Search Result error")
       })

    };    
});

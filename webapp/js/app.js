var myApp = angular.module('myApp', []);

myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                    console.log("MyFile: " + JSON.stringify(scope.myFile))
                    console.log("In directive, scope is ")
                    console.log(scope)
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
    

    $scope.uploadFile = function(){
        console.log("In Ctrl, scope is ")
        console.log($scope)
        var file = $scope.myFile;
        console.log('file is ' + JSON.stringify(file));
        var uploadUrl = "/upload";
        fileUpload.uploadFileToUrl(file, uploadUrl).then(function(data){
            $scope.data = data;
            console.log(data);
        }, function(data){
            console.log("Upload file call back failed")
        });
        
    };    
}]);

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

myApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(event){
            console.log("The file has been successful uploaded")
            console.log(event)
        })
        .error(function(){
            console.log("There is an error uploading the file")
        });
    }
}]);

myApp.controller('uploadCtrl', ['$scope', 'fileUpload', function($scope, fileUpload){
    
    $scope.uploadFile = function(){
        console.log("In Ctrl, scope is ")
        console.log($scope)
        var file = $scope.myFile;
        console.log('file is ' + JSON.stringify(file));
        var uploadUrl = "/upload";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };

    
}])
.controller('mainController', ['$scope', function($scope){
    
    $scope.errorText = " ";
    $scope.totalItems = " ";
    $scope.delay = " ";
    $scope.results = {};
}]);

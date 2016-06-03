var app = angular.module("products",[]);
//FormController is contains the property execSearch, which ranks JSON objects based on the user's Weightage and spits out the top 10 models according to rank.
app.controller("FormController",['$http',function($http){
  var catalogue = this;
  var royalty_level_one = ["Apple","Samsung","Microsoft","LG","OnePlus","Sony","HTC"]; //All top phone brands are given a royalty factor of 1.75 in the final rank calculation
  var royalty_level_two = ["Acer","Amazon","BlackBerry","Dell","Motorola","XOLO","Asus","Xiaomi"]; //All phone brands next to the top ones are given a royalty factor of 1.25 in the final rank calculation.
  //All the royalty rankings are given based on the top 15 phone brands released by Digit - 2015
  this.products = [];
  this.execSearch=function(){
    this.products=[];
    var cameraWeightage = $("#ex1").val();
    var internalWeightage = $("#ex2").val();
    var batteryWeightage = $("#ex3").val();
    var memoryWeightage = $("#ex4").val();
    var arr = [];
    var index = [];
    var flag = 0;
    catalogue.productList = $http.get('gsmdata.json').success(function(data){
      catalogue.productList = data;
      for(var i=0;i<catalogue.productList.results.length;i++)
        index[i] = i;
      for(var i=0;i<catalogue.productList.results.length;i++){
        var rank = (cameraWeightage*(Number(catalogue.productList.results[i].model_camera_specs)/8)) + (batteryWeightage*(Number(catalogue.productList.results[i].model_battery_specs)/2100)) + (memoryWeightage*(Number(catalogue.productList.results[i].model_ram_specs)/2)) + (internalWeightage*(Number(catalogue.productList.results[i].model_internal_storage)/8));
        for(var j=0;j<royalty_level_one.length;j++){
          flag = 0;
          if(catalogue.productList.results[i].model_full_name.includes(royalty_level_one[j])){
            rank = rank*1.75;
            flag = 1;
            break;
          }
        }
        for(var j=0;j<royalty_level_two.length;j++){
          if(flag==1)
            break;
          if(catalogue.productList.results[i].model_full_name.includes(royalty_level_two[j])){
            rank = rank*1.25;
            flag = 1;
            break;
          }
        }
        arr[i] = rank;
      }
      //Applying insertion sort on both the arrays i.e. the rank array and index array which are corresponding to each other,
      //based on the rank we obtain the index for top 10 JSON objects based on rank.
      for(var i=0;i<arr.length;i++){
        for(var j=i+1;j<arr.length;j++){
          if(arr[i]<arr[j]){
            var temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            temp = index[i];
            index[i] = index[j];
            index[j] = temp;
          }
        }
      }
      //This filtering is done to root out repeated objects and the final array contains only 10 unique array objects.
      var topcount=0,j=0;
      while(topcount!=10){
        flag=0;
        for(var i=0;i<catalogue.products.length;i++){
          if((catalogue.products[i].model_full_name==catalogue.productList.results[index[j]].model_full_name)||(catalogue.products[i].model_ram_specs==catalogue.productList.results[index[j]].model_ram_specs && catalogue.products[i].model_camera_specs==catalogue.productList.results[index[j]].model_camera_specs && catalogue.products[i].model_internal_storage==catalogue.productList.results[index[j]].model_internal_storage && catalogue.products[i].model_battery_specs==catalogue.productList.results[index[j]].model_battery_specs)){
            flag = 1;
            break;
          }
        }
        if(flag==1)
          j++;
        else{
          catalogue.products.push(catalogue.productList.results[index[j]]);
          topcount++;
          j++;
        }
      }
      document.getElementById("no-selection").innerHTML = 'Here are your top 10 results';
      document.getElementById("finish").innerHTML = 'That\'s all folks!'
    });
  }
}]);

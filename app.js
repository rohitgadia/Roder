var cameraWeightage,internalWeightage,memoryWeightage,batteryWeightage;
$(document).ready(function(){
var element = document.getElementById('no-selection');
element.innerHTML = 'Nothing here yet!';
cameraWeightage = $("#ex1").slider();
internalWeightage = $("#ex2").slider();
memoryWeightage = $("#ex3").slider();
batteryWeightage = $("#ex4").slider();
});
function getTotalWeightage(){
  var total = cameraWeightage.slider('getValue')+internalWeightage.slider('getValue')+memoryWeightage.slider('getValue')+batteryWeightage.slider('getValue');
  if(total>28){
    $("#form-submit").attr("disabled","disabled");
    var element = document.getElementById('error-span');
    element.innerHTML = 'Please make sure the total Weightage doesn\'t exceed 28';
  }
  else{
    var element = document.getElementById('error-span');
    element.innerHTML = '';
    $("#form-submit").removeAttr("disabled");
  }
}
if($(window).width()>900){
$(window).scroll(function(){
  var current = $("#no-hide").scrollTop();
  var height = $(this).scrollTop();
  if(height==0)
    height = 50;
  setTimeout(function(){
    for(var i = 0;i<=height+50;i=i+height/10){
      $("#no-hide").css("margin-top",current+i);
    }
  },500);
});
}

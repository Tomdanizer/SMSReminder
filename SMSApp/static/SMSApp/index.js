//Main SMS functions
var sms = (function(){
  var selectedCarrier = null;
  var init = function(){
      setupStepTransitionListeners();
      setupControls();
      setupDomEvents();
  },
  setupDomEvents = function(){
      $(document).on("scroll",function(){
        if($(document).scrollTop()>175){
            $("nav").removeClass("menu-row").addClass("menu-row-small");
        } else{
            $("nav").removeClass("menu-row-small").addClass("menu-row");
        }
      });
      
      $( '.menulink' ).on('click', function(event) {
        
        var $target = $("#" + $(this).data('target'));
        if($target.offset() && $target.offset().top){
          event.preventDefault();
          $('html, body').animate({
              scrollTop: $target.offset().top - 50
          }, 500);
        }
      });

      $('img[data-carrier]').click(function(){
         if(selectedCarrier === null){
             selectedCarrier = $("*[class='carrier-selected']").first()
        }
         if(selectedCarrier !== null){
          selectedCarrier.removeClass('carrier-selected');

         }
         selectedCarrier = $(this);
         $('#id_network').val(this.getAttribute("data-carrier"));
         selectedCarrier.addClass('carrier-selected');
         //$('#carrier_selected').text(this.getAttribute("data-carriername") + " selected");
      });
    

  },
  setupControls = function(){
      //Attaches datetime picker to date field
      $('#datetimepicker').datetimepicker();
  },
  setupStepTransitionListeners = function(){
         var $phoneNumberField = $("#id_phone_number");
         var $dateField = $("#id_date");
         var $messageField = $("#id_message");
         var $speech1 = $(".speech").hide();
         var $speech2 = $(".speech2").hide();;
         var $speech3 = $(".speech3").hide();
           
            
            $phoneNumberField.focusin(function(){
              $speech1.show();
              console.log("HI phoneNumberField");
              $speech1.addClass('animated bounceInDown').removeClass("bounceOutUp");
            }).focusout(function(){
               $speech1.addClass("bounceOutUp").removeClass("bounceInDown");
            });
      
            $dateField.focusin(function(){
              $speech2.show();
              $speech2.addClass('animated bounceInRight').removeClass("bounceOutRight");
              $dateField.css("bounceInLeft");
              console.log("HI dateField");
            }).focusout(function(){
               $speech2.addClass('animated bounceOutRight').removeClass("bounceInRight");
            });
            $messageField.focusin(function(){
              $speech3.show();
              $speech3.addClass('animated bounceInUp').removeClass("bounceOutDown");
              console.log("HI messageField");
            }).focusout(function(){
               $speech3.addClass('animated bounceOutDown').removeClass("bounceInUp");
            });
    
            $('.glyphicon-calendar').hover(function(){
                //$dateField.focusout();
            });  
  };
 
  return {
    init: init
  };
})();
$(document).ready(sms.init);
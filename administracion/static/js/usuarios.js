
(function($) {
  "use strict";
  
  $(function(){
    // Input groups example
    var validateInputGroups = $("#form-validation-input-groups").validate({
      // Validation rules
      // Selecting input by name attribute
      rules: {
        inputFirstName2: {
          required: true,
          minlength: 5
        },
        inputEmail2: {
          email: true,
          required: true,
          minlength: 5
        },
        inputUsername2: {
          required: true
        },
        inputPassword2: {
          required: true,
          minlength: 5
        },
      },
      // Error messages
      messages: {
        inputFirstName2: "El nombre es requerido( Al menos 5 caracteres )",
        inputEmail2: "El email es requerido",
        inputUsername2: "El usuario es requerido",
        inputPassword2: "El password es requerido ( Al menos 5 caracteres )"
      },
      highlight: function(element, errorClass, validClass) {
        $(element).closest('.form-group').addClass('has-error').find('label').addClass('control-label');
        $(element).closest(".form-group").find('.input-icon').removeClass('fa-check none').addClass('fa-times');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).closest('.form-group').removeClass('has-error');
        $(element).closest(".form-group").find('.input-icon').removeClass('fa-times').addClass('fa-check');
      },
      // Class that wraps error message
      errorClass: "help-block",
      // Element that wraps error message
      errorElement: "div",
      errorPlacement: function(error, element) {
        $(element).closest(".form-group").append(error);

        // // Select2 validation
        // $("select").on("change", function(){
        //   var select2Valid = $(this).valid();
        //   // If clicked on clear button
        //   if(!select2Valid){
        //     $(this).parent().removeClass("has-success").addClass("has-error");
        //   }
        // });
      },
      success: function(helpBlock) {
        if( $(helpBlock).closest(".form-group").hasClass('has-error') ){
          $(helpBlock).closest(".form-group").removeClass("has-error").addClass("has-success");
        }
      }
    });

    // Advanced example
    var validateAdvanced = $("#form-validation-advanced").validate({
      // Validation rules
      // Selecting input by name attribute
      rules: {
        inputName3: {
          required: true,
          minlength: 5
        },
        inputEmail3: {
          email: true,
          required: true,
          minlength: 5
        },
        inputPassword3: {
          required: true,
          minlength: 5
        },
        inputAddress3: {
          required: true
        },
        inputCity3: {
          required: true
        },
        country3: {
          required: true
        },
        inputZip3: {
          required: true,
          minlength: 2,
          digits: true
        },
        inputCreditCard3: {
          required: true,
          minlength: 16,
          digits: true
        },
        year3: {
          required: true
        },
        description3: {
          required: true,
          minlength: 25
        },
        terms3: {
          required: true
        }
      },
      // Error messages
      messages: {
        inputName3: "Full Name is required ( at least 5 characters )",
        inputEmail3: "Email is required ( at least 5 characters )",
        inputPassword3: "Password is required ( at least 5 characters )",
        inputAddress3: "Address is required",
        inputCity3: "City is required",
        country3: "Country is required",
        inputZip3: "Zip is required",
        inputCreditCard3: "Credit card number is required ( 16 digits )",
        year3: "Credit card year of expiration is required",
        description3: "Description is required ( at least 25 characters )",
        terms3: "You should agree to our Terms Of Use"
      },
      highlight: function(element, errorClass, validClass) {
        $(element).closest('.form-group').addClass('has-error').find('> label').addClass('control-label');
        $(element).closest(".form-group").find('.input-icon').removeClass('fa-check none').addClass('fa-times');
      },
      unhighlight: function(element, errorClass, validClass) {
        $(element).closest('.form-group').removeClass('has-error');
        $(element).closest(".form-group").find('.input-icon').removeClass('fa-times').addClass('fa-check');
      },
      // Class that wraps error message
      errorClass: "help-block",
      // Element that wraps error message
      errorElement: "div",
      errorPlacement: function(error, element) {
        $(element).closest(".form-group").find('> :last-child').append(error);

        // Select2 validation
        $("select").on("change", function(){
          var select2Valid = $(this).valid();
          // If clicked on clear button
          if(!select2Valid){
            $(this).closest('.form-group').removeClass("has-success").addClass("has-error");
          }
        });

        // For Icheck we need revalidate
        if( $(element).is(':checkbox') || $(element).is(':radio') ){
          $(element).on('ifChecked ifUnchecked', function(e){
            validateAdvanced.element($(element));
          });
        }
      },
      success: function(helpBlock) {
        if( $(helpBlock).closest(".form-group").hasClass('has-error') ){
          $(helpBlock).closest(".form-group").removeClass("has-error").addClass("has-success");
        }
      },
      invalidHandler: function(event, validator) {
        // 'this' refers to the form
        var errors = validator.numberOfInvalids();
        if (errors) {
          // Error message
          var message = errors == 1
            ? 'You missed 1 field. It has been highlighted'
            : 'You missed ' + errors + ' fields. They have been highlighted';

          // Page scroll
          $('html, body').animate({
            scrollTop: $(this).closest('.panel').offset().top - $('.navbar-top').height()
          }, 500);

          $(this).find('.alert strong').text(message);
          $(this).find('.alert').removeClass('none');
        }else{
          $(this).find('.alert').addClass('none');
        }
      }
    });
  })
})(jQuery);
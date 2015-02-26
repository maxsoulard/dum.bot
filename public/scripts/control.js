// Constantes ajax

const FORWARD = '/goForward';
const BACKWARD = '/goBackward';
const LEFT = '/turnLeft';
const RIGHT = '/turnRight';

// Constantes actions camera

const C_UP = '/camUp';
const C_DOWN = '/camDown';
const C_LEFT = '/camLeft';
const C_RIGHT = '/camRight';

// Classes CSS

const CSS_BUTTON_DISABLED = "pure-button-disabled";
const CSS_BUTTON_AUTO = "#button-auto";
const CSS_BUTTON_MANUEL = "#button-manuel";
const CSS_BUTTON_RESET = "#button-reset";
const CSS_BUTTON_STOP = "#button-stop";

// pour les joysticks : maps d'actions
var actionsJoystickL = new Array();
actionsJoystickL["up"] = FORWARD;
actionsJoystickL["down"] = BACKWARD;
actionsJoystickL["left"] = LEFT;
actionsJoystickL["right"] = RIGHT;

var actionsJoystickR = new Array();
actionsJoystickR["up"] = C_UP;
actionsJoystickR["down"] = C_DOWN;
actionsJoystickR["left"] = C_LEFT;
actionsJoystickR["right"] = C_RIGHT;

$(document).ready(function(){
    var doingKb = null; // Conserve l'action serveur en cours, commande keyboard

    ///////////////////////////////////
    // Handler sur les boutons
    //////////////////////////////////

	// Init
	$(CSS_BUTTON_AUTO).toggleClass(CSS_BUTTON_DISABLED);

    $(CSS_BUTTON_AUTO).click(function() {
		if (!isButtonDisabled(CSS_BUTTON_AUTO)){
			launchAjaxRequest('/modeAuto');
			$(CSS_BUTTON_AUTO).toggleClass(CSS_BUTTON_DISABLED);
			if (isButtonDisabled(CSS_BUTTON_MANUEL)) {
				$(CSS_BUTTON_MANUEL).toggleClass(CSS_BUTTON_DISABLED);
			}
		}
    });
    $(CSS_BUTTON_MANUEL).click(function() {
        if (!isButtonDisabled(CSS_BUTTON_MANUEL)){
			launchAjaxRequest('/modeManuel');
			$(CSS_BUTTON_MANUEL).toggleClass(CSS_BUTTON_DISABLED);
			if (isButtonDisabled(CSS_BUTTON_AUTO)) {
                $(CSS_BUTTON_AUTO).toggleClass(CSS_BUTTON_DISABLED);
            }
		}
    });
    $(CSS_BUTTON_RESET).click(function() {
        if (!isButtonDisabled(CSS_BUTTON_RESET)){
            launchAjaxRequest('/resetGpio');
			//$.ajax({'url': '/resetGpio'});
			//request.done(function(response){
            //});
        }
    });
    $(CSS_BUTTON_STOP).click(function() {
        if (!isButtonDisabled(CSS_BUTTON_STOP)){
            launchAjaxRequest('/stop');
        }
    });

    var isButtonDisabled = function(buttonId) {
        return $(buttonId).hasClass(CSS_BUTTON_DISABLED);
    }

    ///////////////////////////////////
    // Gestion du clavier
    //////////////////////////////////

    down = {}; // Conserve l'état des touches actionnées
    $(document).on('keydown', function(e) {
        handlerkeyDown(e, 90, FORWARD); // Z
        handlerkeyDown(e, 81, LEFT); // Q
        handlerkeyDown(e, 68, RIGHT); // S
        handlerkeyDown(e, 83, BACKWARD); // D
    });

    $(document).on('keyup', function(e) {
        launchAjaxRequest(doingKb);
        doingKb = null;
        down[e.keyCode] = null;
    });

    var handlerkeyDown = function(e, keyCode, action) {
        if (e.which === keyCode && down[keyCode] == null && doingKb == null) {
            launchAjaxRequest(action);
            down[keyCode] = true;
            doingKb = action;
        }
    };

    var launchAjaxRequest = function(url) {
        if (url != null) {
            var request = $.ajax({'url': url});
            request.done(function(response){
            });
        }
    };

    ///////////////////////////////////
    // Gestion du joystick gauche (moteurs)
    //////////////////////////////////

    var doingJsL = new Doing();
    var baseXJoystickL = null;
    var joystickL	= new VirtualJoystick({
        container	: document.getElementById('container'),
		stickElement : document.getElementById('stickcontainer'),
        strokeStyle	: 'cyan',
        limitStickTravel: true,
        stickRadius     : 120
    });

    joystickL.addEventListener('touchStartValidation', function(event){
		var touch	= event.changedTouches[0];
		if( touch.pageX >= window.innerWidth/2 )	return false;
		baseXJoystickL = touch.pageX;
		return true
	});

	///////////////////////////////////
    // Gestion du joystick droit (caméra)
    //////////////////////////////////

    var doingJsR = new Doing();
    var baseXJoystickR = null;
    var joystickR	= new VirtualJoystick({
        container	: document.getElementById('container'),
		stickElement : document.getElementById('stickcontainer'),
        strokeStyle	: 'orange',
        limitStickTravel: true,
        stickRadius     : 120
    });

    joystickR.addEventListener('touchStartValidation', function(event){
		var touch	= event.changedTouches[0];
		if( touch.pageX < window.innerWidth/2 )	return false;
		baseXJoystickR = touch.pageX;
		return true
	});

    ///////////////////////////////////
    // Appel des handlers sur les deux joysticks
    //////////////////////////////////

    animate();
    function animate(){
        requestAnimationFrame(animate);
        handlerJoystickStart(joystickR);
        handlerJoystickStart(joystickL);
    }

    joystickR.addEventListener('touchEnd', function(event){
        handlerJoystickEnd(joystickR);
    });

    joystickL.addEventListener('touchEnd', function(event){
        handlerJoystickEnd(joystickL);
    });

	//handlerJoystickEnd(joystick, doingJsL, actionsJoystickL, event));
    //joystick.addEventListener('touchEnd', handlerJoystickEnd(joystick, doingJsR, actionsJoystickR, event));

	///////////////////////////////////
    // Joystick - commun
    //////////////////////////////////

    function handlerJoystickEnd(joystick) {
        var determineJoystick = new DetermineJoystick(joystick._baseX);
	var doing = determineJoystick.doing;
        var actionsJoystick = determineJoystick.actionsJoystick;

        Object.keys(actionsJoystick).forEach(function(entry) {
            strToEval = "if (joystick."+entry+"()){launchAjaxRequest('"+actionsJoystick[entry]+"');}";
            eval(strToEval);
            doing.value = null;
        });
    }

    function handlerJoystickStart(joystick) {
        var determineJoystick = new DetermineJoystick(joystick._baseX);
	var doing = determineJoystick.doing;
        var actionsJoystick = determineJoystick.actionsJoystick;

        if (joystick.up() && doing.value != actionsJoystick["up"]) {
            launchAjaxRequest(doing.value);
	        doing.value = actionsJoystick["up"];
            launchAjaxRequest(doing.value);
        }
        else if (joystick.down() && doing.value != actionsJoystick["down"]) {
            launchAjaxRequest(doing.value);
            doing.value = actionsJoystick["down"];
            launchAjaxRequest(doing.value);
        }
        else if (joystick.left() && !joystick.down() && !joystick.up() && doing.value != actionsJoystick["left"]) {
            launchAjaxRequest(doing.value);
            doing.value = actionsJoystick["left"];
            launchAjaxRequest(doing.value);
        }
        else if (joystick.right() && !joystick.down() && !joystick.up() && doing.value != actionsJoystick["right"]) {
            launchAjaxRequest(doing.value);
            doing.value = actionsJoystick["right"];
            launchAjaxRequest(doing.value);
        }
    }

    function DetermineJoystick(basex){
        if( basex < window.innerWidth/2 ) {
            this.doing = doingJsL;
            this.actionsJoystick = actionsJoystickL;
        }
        else if( basex >= window.innerWidth/2 ) {
            this.doing = doingJsR;
            this.actionsJoystick = actionsJoystickR;
        }
        else {
            this.doing = null;
        }
    }

    function Doing(value) {
        this.value = value;
    }


});


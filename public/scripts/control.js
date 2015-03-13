// Constantes
// ajax

const FORWARD = '/goForward';
const BACKWARD = '/goBackward';
const LEFT = '/turnLeft';
const RIGHT = '/turnRight';

// Kb actions
keyCodes = {'up':90, 'down':68, 'left':81, 'right':83}
actionsKb = {keyCodes['up']:FORWARD, keyCodes['down']:BACKWARD, keyCodes['left']:LEFT, keyCodes['right']:RIGHT}

// actions camera

const C_UP = '/camUp';
const C_DOWN = '/camDown';
const C_LEFT = '/camLeft';
const C_RIGHT = '/camRight';
const C_CENTER = '/camCenter';

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
actionsJoystickR["center"] = C_CENTER;

$(document).ready(function(){
    var doingKb = null; // Conserve l'action serveur en cours, commande keyboard

	///////////////////////////////////
	// Mjpeg stream img
	////////////////////////

	$("#stream").attr("src","http://"+document.location.hostname+":8083/?action=stream")

    ///////////////////////////////////
    // Handler sur les boutons
    //////////////////////////////////

	// Init
	$(CSS_BUTTON_MANUEL).toggleClass(CSS_BUTTON_DISABLED);

    $(CSS_BUTTON_AUTO).click(function() {
		if (!isButtonDisabled(CSS_BUTTON_AUTO)){
			fireAjaxRequest('/modeAuto');
			$(CSS_BUTTON_AUTO).toggleClass(CSS_BUTTON_DISABLED);
			if (isButtonDisabled(CSS_BUTTON_MANUEL))    $(CSS_BUTTON_MANUEL).toggleClass(CSS_BUTTON_DISABLED);
		}
    });
    $(CSS_BUTTON_MANUEL).click(function() {
        if (!isButtonDisabled(CSS_BUTTON_MANUEL)){
			fireAjaxRequest('/modeManuel');
			$(CSS_BUTTON_MANUEL).toggleClass(CSS_BUTTON_DISABLED);
			if (isButtonDisabled(CSS_BUTTON_AUTO))      $(CSS_BUTTON_AUTO).toggleClass(CSS_BUTTON_DISABLED);
		}
    });
    $(CSS_BUTTON_RESET).click(function() {
        if (!isButtonDisabled(CSS_BUTTON_RESET))    fireAjaxRequest('/resetGpio');
    });
    $(CSS_BUTTON_STOP).click(function() {
        if (!isButtonDisabled(CSS_BUTTON_STOP))     fireAjaxRequest('/stop');
    });

    var isButtonDisabled = function(buttonId) {
        return $(buttonId).hasClass(CSS_BUTTON_DISABLED);
    }

    ///////////////////////////////////
    // Gestion du clavier
    //////////////////////////////////

    down = {}; // Conserve l'état des touches actionnées
    $(document).on('keydown', function(e) {
        handlerkeyDown(e, keyCodes['up']); // Z
        handlerkeyDown(e, keyCodes['left']); // Q
        handlerkeyDown(e, keyCodes['down']); // S
        handlerkeyDown(e, keyCodes['right']); // D
    });

    $(document).on('keyup', function(e) {
        if (e.which === keyCodes['up'] || e.which === keyCodes['down']) {
            fireAjaxRequest(doingKb);
            doingKb = null;
            down[e.keyCode] = null;
        }
    });

    var handlerkeyDown = function(e, keyCode) {
        if (e.which === keyCode && down[keyCode] == null && doingKb == null) {
            fireAjaxRequest(actionsKb[keyCode]);
            down[keyCode] = true;
            doingKb = actionsKb[keyCode];
        }
    };

    var fireAjaxRequest = function(url) {
        if (url != null)    var request = $.ajax({'url': url});
    };

    ///////////////////////////////////
    // Gestion du joystick gauche (moteurs)
    //////////////////////////////////

    var doingJsL = {};
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

    var doingJsR = {};
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

        if (doing.value == actionsJoystick["up"] || doing.value == actionsJoystick["down"]) fireAjaxRequest(doing.value);
        doing.value = null;

//        Object.keys(actionsJoystick).forEach(function(entry) {
//            strToEval = "if (joystick."+entry+"()){fireAjaxRequest('"+actionsJoystick[entry]+"');}";
//            eval(strToEval);

//            fireAjaxRequest(actionsJoystick[entry]);

//            doing.value = null;
//        });
    }

    function handlerJoystickStart(joystick) {
        var determineJoystick = new DetermineJoystick(joystick._baseX);
	    var doing = determineJoystick.doing;
        var actionsJoystick = determineJoystick.actionsJoystick;

        if (joystick.up() && doing.value != actionsJoystick["up"])          actionStick("up");
        else if (joystick.down() && doing.value != actionsJoystick["down"]) actionStick("down");
        else if (joystick.left() && !joystick.down() && !joystick.up() && doing.value != actionsJoystick["left"]) actionStick("left");
        else if (joystick.right() && !joystick.down() && !joystick.up() && doing.value != actionsJoystick["right"]) actionStick("right");

//      TODO re centrer camera
//        if (!joystick.center()) {
//        }
//        else if (doing.value != actionsJoystick["center"]) {
//			console.log("center");
//            actionStick("center");
//            determineJoystick.isJoystickR = false;
//        }
        function actionStick(actionKey){
            fireAjaxRequest(doing.value);
            doing.value = actionsJoystick[actionKey];
            fireAjaxRequest(doing.value);
        }
    }

    function DetermineJoystick(basex){
        if( basex < window.innerWidth/2 ) {
            this.isJoystickR = false;
            this.doing = doingJsL;
            this.actionsJoystick = actionsJoystickL;
        }
        else if( basex >= window.innerWidth/2 ) {
            this.doing = doingJsR;
            this.isJoystickR = true;
            this.actionsJoystick = actionsJoystickR;
        }
        else    this.doing = null;
    }

    function Doing(value) {
        this.value = value;
    }


});


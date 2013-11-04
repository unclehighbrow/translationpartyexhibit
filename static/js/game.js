var PANEL_ANIM = {
	hide: function($panel){
		$panel.transition({scale: .6, opacity: 0}, 200, 'easeOutBack');
	},
	show: function($panel){
		$panel.transition({scale: 1, opacity: 1}, 200, 'easeOutBack');					
	},
	set: function($panel){
		$panel.transition({scale: .6, opacity: 0}, 0);
	},
	reset: function($panel){
		$panel.transition({scale: 1, opacity: 1}, 0);
	}
};


function Party() {
	this.when_party_busted = function(){
	// console.log('party busted, default ending');
	};
	this.phrase_queue = [];
	this.last_displayed_phrase = 0;
	this.party_status = 'partying';
	this.partier = {};
};

Party.prototype = {
	translation_tpl: $('#translation_tpl').html(),
	quip_types : [
		{ 
			'type': 'uppercase',
			'match': /^[A-Z\s.\?\!]+$/,
			'quips': [
				"But it's not nice to shout in Japanese, either."
			]
		},
		{ 
			'type': 'meme',
			'match': /(all your base|i can ha[sz]+|never gonna|not sure if|i don't always)/i,
			'quips': [
				"You're sure are up on your Internet jokes!",
				"That Internet joke is funny in any language!"
			]
		},
		{
			'type': 'museum', 
			'match': /(museum|moving image|movingimage|MovingImageNYC|\bmmi\b)/i,
			'quips': [
				"It's a pretty cool museum, isn't it?"
			]
		},
		{
			'type': 'multipurpose',
			'match': /.*/,
			'quips': [
				"This is a real translation party!",
				"You should move to Japan!",
				"That's deep, man.",
				"Come on, you can do better than that.",
				"That didn't even make that much sense in English."
			]
		}
	],
	
	
	// translating side
	// all translating is happening on the backend now
	/*
	translate_last_phrase: function(){
		var phrase = this.phrase_queue[this.phrase_queue.length - 1];
		var outLang = (phrase.lang == 'en') ? 'ja' : 'en';
		var self = this;
		
		var translation_success = function(result){
		// console.dir(result);
		self.handle_translation_response(result, outLang);
		}
		
		var translation_fail = function(result){
		// console.dir(result);
		alert("problem with Bing, probably over limit");
		}
		
		$.ajax({
			url: 'http://api.microsofttranslator.com/V2/Ajax.svc/GetTranslations', 
			data: {
				'appId' : 'F2926FC35C3732CEC3E9C92913745F9C28912821',
				'text'	: phrase.string,
				'from'	: phrase.lang,
				'to'	: outLang,
				'maxTranslations' : 1,
			},
			dataType: 'jsonp',
			jsonp : 'oncomplete',
			success: translation_success,
			error: translation_fail
		});
	},
	
	handle_translation_response: function(result, outLang){
		this.phrase_queue.push({
		'lang': outLang,
		'string': result.Translations[0].TranslatedText
		});
		this.check_party_progress();
	},
	*/
	

	check_column: function($col){
		var $cards = $col.find('.card');
		var max_cards =	 ( $col.parent().parent().is('.col:last') ) ? (CARDS_PER_COLUMN - 1) : CARDS_PER_COLUMN;
		if( $cards.length > max_cards ){
			var $excess_card = $cards.first();
			var $excess_card_clone = $excess_card.clone();
			this.add_card( $col.parent().parent().prev().find('.frame'), $excess_card_clone, function(){
				$excess_card.remove();
			});
		}
	},
	
	add_card: function( $col, $card, callback ){
		$card.appendTo($col).hide();
		var self = this;
		var callback = callback || function(){};
		setTimeout(function(){
			$card.show();
			$col.transition({y: CARD_HEIGHT}, 0);
			$col.transition({y: 0}, 200, function(){
				$card.removeClass('new');
				callback();
			});		
			self.check_column($col);	
		}, 0);
	},

	// displaying side 
	display_available_phrase: function(){
		// no "phrase limit" per se, if no equilibrium is reached by the end of the queue, then it's a bust

		if( this.phrase_queue.length > this.last_displayed_phrase ){
			var phrase = this.phrase_queue[this.last_displayed_phrase];
			$t = $( Mustache.render(this.translation_tpl, {t: phrase.string, l: this.get_language(phrase.lang, this.last_displayed_phrase)}) );	 
			this.add_card( $('.col:last .frame'), $t);
			this.last_displayed_phrase++;
			this.check_party_progress();
		}
		else{
		
			//there won't be any more translations coming, so this party is over 
			this.bust_this_party();
			
			var quip, type, type_message;
			if( this.party_status == 'equilibrium' ){
				// it hit equilibrium 
				$('.last_col .frame .card').css({background: 'lightgreen'});
				quip = this.get_quip( this.phrase_queue[0].string ); // quip based on original input
				type = 'success';
				type_message = "Equilibrium found!"
			}
			else{
				// ran out before it made it
				quip = 'It is unlikely that this phrase will ever reach equilibrium';
				type = 'abject_failure';
				type_message = "Party is busted!"
			}
			
			// flip translator and end the party
			$('#translator .back').addClass(type);
			$('#quip').html(quip);
			$('#type_message').text(type_message);
			$('#translator').addClass('flipped');
		}
	},

	// what next?
	check_party_progress: function(){
		if( this.phrase_queue.length > 3 && 
			this.phrase_queue[this.phrase_queue.length - 1].lang == 'en' && 
			this.phrase_queue[this.phrase_queue.length - 1].string ==	 this.phrase_queue[this.phrase_queue.length - 3].string 
		){
		// reached equilibrium
			this.party_status = 'equilibrium';
		}
		else if(this.phrase_queue.length >= PHRASE_LIMIT){
			// hit the limit
			this.party_status = 'limit';
		}
		else{
			// carry on then
		
			// and by carry on, I mean do nothing. all translating is happening on the backend now.
			/* this.translate_last_phrase(); */
		}
	},

	kill_phrases: function(callback){
		
		var $cards = $('.card');
		var this_card = 0;
		var interval = 50;

		// show cols
		var hide_next_card = function(){
			// $($cards[this_card]).css({visibility: 'hidden'});
			$($cards[this_card]).transition({opacity: 0, y: 300, rotate: 30 }, 300);
			this_card++
			if(this_card < $cards.length){
				setTimeout(hide_next_card, interval);
			}
			else{
				// no more cards to hide, we're done here
				setTimeout(function(){
					$('.col').empty();
					if(callback){
						callback.apply(this);							
					}
				}, HEARTBEAT_TIME * 3);
			}
		}
		hide_next_card();
		
	},
	
	get_quip: function(phrase){						
		var quips, rand;
		for (var i=0; i<this.quip_types.length; i++){
			if( phrase.match(this.quip_types[i].match) ){
			quips = this.quip_types[i].quips;
			// console.log('matched quip type: '+this.quip_types[i].type);
			break;
			}
		}

		rand = Math.floor(Math.random()*(quips.length));
		return quips[rand];
	},

	get_language: function(l, index){
		if(l == 'en'){
			if(index == 0){
				return "";
			}
			else{
				return "back into English";
			}
		}
		else{
			return "into Japanese";
		}
	},


	
	// init
	get_this_party_started: function( partydata ){
		// re-add frames
		$('.col').append('<div class="wrap"><div class="frame" /></div></div>');

		// set up data
		if( typeof partydata.phrase_queue !== 'undefined' ){
			// this is a premade attract-mode party
			this.phrase_queue = partydata.phrase_queue;
		}
		else{
			// this isn't a premade attract-mode party
			this.phrase_queue.push({
			'lang': 'en',
			'string': partydata.t
			});
					}
			this.partier = partydata.partier;

			// do initial display of phrase
			var $translator = $(Mustache.render( $('#newphrase_tpl').html(), partydata));
			var $col_last = $('.col:last');
			$translator.appendTo($col_last.find('.wrap')).height( $col_last.height() );
			PANEL_ANIM.set($translator);
			PANEL_ANIM.show($translator);

			$col_last.find('.frame').css({paddingBottom: CARD_HEIGHT });
			$('#translating').hide();
		
			// ok, enough of that
		
			var self = this;
			setTimeout(function(){
				$translator.transition({height: (CARD_HEIGHT - 16)}, 200, function(){
				$('#translating').show();
				$('#announcing').hide();
			
				/*
				$('#translating h2').rainbow({ 
					colors: [
						'rgba(255,255,255,.5)',
								'rgba(255,255,255,.7)',
						'rgba(255,255,255,1)'
					],
					animate: true,
					animateInterval: 200,
					pad: false,
					pauseLength: 100,
				});
				*/
			
				// kick off the translating
				self.display_available_phrase(); // do one quickly to start
				self.display_interval = setInterval(function(){
				self.display_available_phrase();
			}, HEARTBEAT_TIME);
			});

		}, HEARTBEAT_TIME * 3);
				

	},
	
	// stop -- translating and displaying is completely done
	bust_this_party: function(){
		clearInterval(this.display_interval);
		var self = this;
		setTimeout(function(){
		self.kill_phrases( self.when_party_busted	 );
		}, BETWEEN_PARTIES_TIME);
	}
	
};


// party host = this is the controller 
var HEARTBEAT_TIME = 2000;
var BETWEEN_PARTIES_TIME = 8000;
var CARDS_PER_COLUMN = 4;
var COLUMNS = 4;
var PHRASE_LIMIT = (CARDS_PER_COLUMN * COLUMNS) - 1;
var CARD_HEIGHT = 220;

function Party_host(){
	// console.log("hi, i'm the party host.");
	this.party_queue = [];
	this.high_water_id = 1;
	this.party_count = 0;
}

Party_host.prototype = {
	
	fetch_new_parties: function(){
		var self = this;
		$.ajax({
			url: 'ajax', 
			data: {'op': 'getNewerThanId', 'id': this.high_water_id},
			dataType: 'json',
			jsonp : 'oncomplete',
			success: function(data){
				if(typeof data.phrases != 'undefined' && data.phrases.length > 0){
					self.add_to_queue(data.phrases);
					self.high_water_id = data.phrases[data.phrases.length - 1].id;
					console.log(data.phrases.length);
				}
			}
		});
	},
	
	fetch_fake_party: function(){
		var fake_party = lol_translations[ Math.floor(Math.random() * lol_translations.length) ];
		this.add_to_queue( [fake_party] );
	},
	
	add_to_queue: function(newparties){
		this.party_queue.push.apply(this.party_queue, newparties);
	},
	
	shift_party_from_queue: function(){
		var p = this.party_queue.shift();
		return p;
	},	

	show_promo: function(callback){
		PANEL_ANIM.set( $('.col') ); 
		$('.unit:even').html( $('#promo_tpl').html() );
		$('.unit:odd').html( $('#gif_tpl').html() );
	
		var $cols = $('.col');
		var this_col = $cols.length - 1;
		var interval = 150
	
		// show cols
		var show_next_col = function(){
			PANEL_ANIM.show( $($cols[this_col]) );
			this_col--;
			if(this_col >= 0){
				setTimeout(show_next_col, interval);
			}
		}
		show_next_col();
	
		//hide cols
		var self = this;
				setTimeout(function(){
			var hide_next_col = function(){
				PANEL_ANIM.hide( $($cols[this_col]) );
				this_col++;
				if(this_col < $cols.length){
					setTimeout(hide_next_col, interval);
				}
				else{
					setTimeout(function(){
						$cols.empty();
						PANEL_ANIM.reset( $cols );
						callback.apply(self);									
					}, BETWEEN_PARTIES_TIME * .33);
				}
			}
			hide_next_col();
		}, BETWEEN_PARTIES_TIME);	
	},
	
	consider_next_party: function(){
		this.fetch_new_parties();
		if( this.party_count % 3 == 0){ 
			this.show_promo(this.consider_next_party);
		}
		else{
			if(this.party_queue.length == 0){
				this.fetch_fake_party();
			}
			this.host_next_party();
		}
		this.party_count++;
	},
	
	host_next_party: function(){
		var p = new Party();
		var self = this;
		p.when_party_busted = function(){
			self.consider_next_party();
		};
		p.get_this_party_started( this.shift_party_from_queue() );
	},

	
	init: function(){
		var self = this;
		$.ajax({
			url: 'ajax', 
			data: {'op': 'getRecent'},
			dataType: 'json',
			jsonp : 'oncomplete',
			success: function(data){
				if(typeof data.phrases != 'undefined' && data.phrases.length > 0){
					self.add_to_queue(data.phrases);
					self.high_water_id = data.phrases[0].id; // in this case, first phrase is the newest phrase
				}
				self.consider_next_party();
			}
		});
	}
	
}
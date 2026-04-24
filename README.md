## Įžanga

###  Kokią programą aš sukūriau?
Mano pasirinkiams yra kortu žaidiams Durnius, angliškai vadinamas Durak. Žaidime reikia žaisti prieš kompiuterio valdomus oponentus ir stengtis pirmam atsikratyti visų kortų. Atkartotos visos pagrindinės žaidimo funkcijos: puolimas, ginyba, primetimai. Kompiuteriu valdomų oponentų logika yra paprasta, bet jos užtenka, jog žaidiams nesijaustų per daug lengvas. Taip pat laimėjimai ir pralaimėjimai yra fiksuojami JSON faile.

###  Kaip paleisti programą?
Kad programa pasileistu, kompiuteryje reikai turėti instaliavus Python kompiliatorių. Tada, naudojant pip ( package installer for Python) reikia instaliuoti biblioteką colorama:

pip install colorama

Tada, reikai nueiti į programos direktoriją ir paleisti pagrindinį kodą Durnius.py:

python Durnius.py


###  Ką daryti atsidarius programą?
Paleidus kodą atsidarys konsolės langas ir jame bus matomi 3 pasirinkimai:
1. **Play** - Įvedus skaičių 1 iššoks pasirinkiams su kiek kompiuterio kontroliuojamų žaidėju norite žaisti (nuo 1 iki 5).
2. **Stats** - Įvedus skaičių 2 galima pamatyti savo žaidimų statistiką: kiek žaidimų laimėta, kiek pralaimėta ir koks laimėjimų procentas.
3. **Exit** - Įvedus skaičių 3 programa bus uždaroma.

Žaidimo metu konsolėje bus rašomi veiksmai kuriuos reikia padaryti.

##

### Kaip šis žaidimas atitinka iškeltus reikalavimus.

- Enkapsulaicija: 
Klasėje Player privatūs atributai yra _name ir _card. Tai neleidžia įsivelti klaidai, kai yra rušioujama žaidėjo ranka. Enkapsuliaciaj neleižia šitų atributų pasiekti niekam kitam tik klasei Player. Pavyzdys:

class Player:
    def __init__(self, name):
        self._name = name  # Kontroliuojama prieiga
        self._hand = []    # Kontroliuojama prieiga

    def add_card(self, card):
        if card:
            self._hand.append(card)
            self._hand.sort(key=lambda c: (c.value(), c.suit))  

    def get_hand(self):
        return self._hand  # Kontroliuojama prieiga
  
- Paveldėjimas: 
Paveldėjimas (Inheritance) panaudojamas norint sukurti kalsė PCPlayer, tai tam, kad nereikėtų kurti naujų atributų ir metodu panaudojamas paveldėjiams ir kviečiama Player klasė.

class PCPlayer(Player):  # Iškviečiama Player klasė
    def choose_attack(self, game):
        if not game.table:
            return min(self._hand, key=lambda c: c.value())  # Paveldi _hand
         ...

    def choose_defense(self, attack_card, game):
        valid = [c for c in self._hand if game.valid_defense(c, attack_card)]  # Paveldi _hand
        return min(valid, key=lambda c: c.value()) if valid else None

-Polimorfizmas

Abstrakti klasė Role apibrėžia metodą play(), kuris skirtingai įgyvendinamas klasėse Attacker ir Defender. Metode DurakGame.play_round() tas pats play() kvietimas polimorfiškai apdoroja tiek žmogaus, tiek kompiuterio žaidėjus. Be to, Player ir PCPlayer turi bendrą sąsają, tačiau elgiasi skirtingai (pavyzdžiui, kompiuteris naudoja jam parašytą specialią logiką).“

class Role(ABC):
    @abstractmethod
    def play(self, game):  # bendras play()
        pass

class Attacker(Role):
    def play(self, game):  # play() panaudojimas atakuojant
        p = game.current_player
        if isinstance(p, PCPlayer):
            # Vykdoma kompiuterio logika
        else:
            # Nuskaitomas žmogaus veiksmas

class Defender(Role):
    def play(self, game):  # play() naudojamas ginantis
        

#
self.current_player = attacker
success = Attacker().play(self)  # vėl kviečiamas play() metodas

- Abstrakcija
Klasė Role yra abstrakti ir apibrėžia metodą play(), tačiau jo naįvykdo. Poklasės (Attacker, Defender) įvykdo tą praleista konkretų kodą. Tai supaprastina žaidimo logiką, leidžiant DurakGame klasei vykdyti tik žaidimo eigai svarbias komandas, nežinant konkrečių puolimo ar gynybos detalių kitaip sakant neapkraunant jos dar daugiau informacijos kurią reiktų apdoroti.

class Role(ABC):
    @abstractmethod
    def play(self, game):  # Abstraktus metodas, nusako ką reikia daryti, bet nepriskiria to jokiai konkrečiai klasei.
        pass

class Attacker(Role):
    def play(self, game):  # išsikviečia play metoda, bet jau atitinkamai klasei Attacker
       
### Design Pattern: Factory metodas

 CardFactory supaprastina kaladės sukūrimą. Vietoje to, kad kiekvienam atvejui t.y. žaidėjų skaičiui būtų aprašomas atskiras kaladės sukūrimo būdas, CardFactory yra vienas, tik kuriant kaladę jam nusiunčiami reikalaviami priklausomai nuo žaidėjų skaičiaus.

class CardFactory:
    @staticmethod
    def create_deck(ranks=None):  # Sukuriamas metodas kuris kuria kaladę pagal nurodytus parametrus
        ranks = ranks or Card.RANKS
        return [Card(s, r) for s in Card.SUITS for r in ranks]

class Deck:
    def __init__(self, ranks=None):
        self.cards = CardFactory.create_deck(ranks)  # Panaudoja Factory
        ...

### Kompozicija ir Agregacija

Kompozicija žaidime pasireiškia, kai klasėje DurakGame sukuriama kaladė, nes gaunasi taip, kad jei tuo metu sukurtas žaidimas ištrinamas išsitrina ir sukurta kaladė. Bet tuo tarpu žaidėjai į klasę DurakGame ateina iš išorės, tad jie gali egzistuoti ir be DurakGame.

class DurakGame:
    def __init__(self, players, ranks=None):
        self.deck = Deck(ranks)  # Kompozicija - DurakGame priklauso sukurta kaladė
        self.players = players   # Agregacija - ima players sukurtus už DurakGame ribų
        self.table = []          # Kompozicija- DurakGame valdo stalą, stalas neegzituoja be DurakGame

### Rašymas ir skaitymas į/ iš failo.

Pasibaigus žaidimui programa uzfiksuoja ar žmogus laimėjo ar pralaimėjo žaidimą ir atitinkamai papildo sukurtą JSON failą.

def update_stats(self, winner):
    file = "stats.json"
    stats = {"games": 0, "human": 0, "pc": 0}
    try:
        with open(file, "r", encoding='utf-8') as f:
            stats = json.load(f)  # Read from file
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    stats["games"] += 1
     ...
    with open(file, "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=4)  # Rašymas į failą

def show_stats(self):
    try:
        with open("stats.json", "r", encoding='utf-8') as f:
            stats = json.load(f)  # Perskaitymas ir statistikos parodymas
         ...




##  Rezultatas ir apibendrinimas

### Rezultatas
- Paleidus programą galima sužaisti veikiančią Diurniaus versiją.
- Kompiuterio valdomas žaidėjas yra tikrai pakankamai protingas ir laimėti nėra taip paprasta kaip atrodo.
- Norėjau padaryti pilną GUI šio žaidimo versiją, bet dėl žinių trūkumo teko tai atidėti kitam kartui, pasirodė per sunku.
- Kartais buvo sunku suprasti kodėl programa neveikia ir ieškoti tos problemos tarp kodo eilučių.


###
-Programas kurti yra sunku.
-Bibliotekos labai pagelbėja.
-Padėjo įsivaizduoti kaip maždaug atrodo žaidimo kodas, kad ir paprastas.

###  Ką būtų galima pagerinti?
- Parašyti geresnią PC žaidėjo logiką.
- Pridėti GUI, tai tikrai pagyvintų ir supaprastintų visą žaidimą iš vizualinės pusės. Būtų tiesiog maloniau žaisti negu dabar.
- Sukurti žaidimo versiją kurią galėtų žaisti keli žmonės iš skirtingų kompiuterių.
- Pridėti durninimą ir persiuntimą.
- Galimybę pasirinkti žaidimo sunkumą.

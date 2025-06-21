# Car models data
models = {
    "Maruti": ["Alto", "Swift", "Baleno", "Dzire", "Ertiga", "Vitara Brezza"],
    "Hyundai": ["i10", "i20", "Creta", "Venue", "Verna", "Elantra"],
    "Tata": ["Nexon", "Harrier", "Tiago", "Punch", "Altroz", "Safari"],
    "Honda": ["City", "Amaze", "Jazz", "WR-V", "BR-V"],
    "Toyota": ["Innova", "Fortuner", "Glanza", "Urban Cruiser", "Camry"],
    "Mahindra": ["XUV300", "XUV700", "Bolero", "Thar", "Scorpio", "XUV500"],
    "Renault": ["Duster", "Kwid", "Triber", "Captur", "Kiger", "Kaptur"],
    "Kia": ["Sonet", "Seltos", "EV6", "EV5", "EV9", "EV4"],
    "Jeep": ["Compass", "Grand Cherokee", "Wrx", "Meridian", "Gladiator", "Wagoneer"],
    "Nissan": ["Kicks", "Terrano", "Duster", "Qashqai", "Juke", "X-Trail"],
    "Skoda": ["Octavia", "Superb", "Kodiaq", "Karoq", "Kodiaq", "Karoq"],
    "Volkswagen": ["Tiguan", "Taigun", "Taigun", "Taigun", "Taigun", "Taigun"],
    "Volvo": ["S60", "S90", "V70", "V90", "V90", "V90"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLB", "GLC", "GLE"],
    "BMW": ["3 Series", "5 Series", "7 Series", "X1", "X3", "X5"],
    "Audi": ["A3", "A4", "A5", "A6", "A7", "A8"],
    
}

# Location data
locations = {
  "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Kakinada", "Vizianagaram", "Srikakulam", "Eluru", "Nandyal", "Kadapa", "Anantapur", "Tirupati", "Rajahmundry", "Ongole", "Chittoor", "Tadepalligudem", "Tadepalle", "Mangalagiri", "Tadikonda"],
  "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang", "Ziro", "Miao", "Bomdila", "Along", "Tezu", "Aalo", "Daporijo", "Anini", "Hayuliang", "Changlang", "Khonsa", "Roing", "Seppa", "Yingkiong", "Basar", "Dirang"],
  "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur", "Bongaigaon", "Karimganj", "Dhubri", "North Lakhimpur", "Sivasagar", "Diphu", "Goalpara", "Barpeta", "Haflong", "Golaghat", "Nalbari", "Morigaon", "Hojai", "Mangaldoi", "Dhemaji", "Hailakandi", "Kokrajhar", "Udalguri"],
  "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga", "Arrah", "Begusarai", "Katihar", "Munger", "Chapra", "Bettiah", "Motihari", "Sitamarhi", "Saharsa", "Hajipur", "Siwan", "Samastipur", "Madhubani", "Purnia", "Aurangabad"],
  "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Durg", "Korba", "Jagdalpur", "Raigarh", "Ambikapur", "Dhamtari", "Rajnandgaon", "Mahasamund", "Kanker", "Janjgir", "Kawardha", "Balod", "Baloda Bazar", "Bemetara", "Bijapur", "Dantewada", "Kondagaon"],
  "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda", "Mormugao", "Sanquelim", "Bicholim", "Valpoi", "Cuncolim", "Curchorem", "Canacona", "Pernem", "Sanguem", "Quepem", "Siolim", "Aldona", "Calangute", "Candolim", "Colva"],
  "Gujarat": ["Ahmedabad", "Surat", "Rajkot", "Vadodara", "Gandhinagar", "Jamnagar", "Bhavnagar", "Junagadh", "Anand", "Nadiad", "Morbi", "Bharuch", "Navsari", "Valsad", "Vapi", "Gandhidham", "Bhuj", "Palanpur", "Himmatnagar", "Godhra"],
  "Haryana": ["Faridabad", "Gurugram", "Panipat", "Ambala", "Rohtak", "Hisar", "Karnal", "Yamunanagar", "Sonipat", "Panchkula", "Bhiwani", "Sirsa", "Bahadurgarh", "Jind", "Thanesar", "Rewari", "Palwal", "Narnaul", "Kaithal", "Hansi"],
  "Himachal Pradesh": ["Shimla", "Dharamshala", "Mandi", "Solan", "Kullu", "Manali", "Palampur", "Chamba", "Bilaspur", "Una", "Hamirpur", "Nahan", "Kangra", "Dalhousie", "Kasauli", "Parwanoo", "Paonta Sahib", "Rampur", "Theog", "Rohru"],
  "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh", "Deoghar", "Giridih", "Ramgarh", "Medininagar", "Chatra", "Gumla", "Lohardaga", "Simdega", "Pakur", "Sahebganj", "Godda", "Dumka", "Jamtara", "Koderma", "Latehar"],
  "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi", "Gulbarga", "Davanagere", "Bellary", "Bijapur", "Shimoga", "Tumkur", "Raichur", "Bidar", "Hospet", "Gadag", "Hassan", "Mandya", "Udupi", "Chitradurga", "Kolar"],
  "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Alappuzha", "Kottayam", "Palakkad", "Malappuram", "Kannur", "Manjeri", "Thalassery", "Kasaragod", "Kayamkulam", "Neyyattinkara", "Ponnani", "Taliparamba", "Varkala", "Changanassery", "Payyannur"],
  "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna", "Ratlam", "Rewa", "Murwara", "Singrauli", "Burhanpur", "Khandwa", "Chhindwara", "Morena", "Bhind", "Guna", "Shivpuri", "Vidisha"],
  "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Amravati", "Kolhapur", "Nanded", "Sangli", "Jalgaon", "Akola", "Latur", "Dhule", "Ahmednagar", "Chandrapur", "Parbhani", "Ichalkaranji", "Jalna"],
  "Manipur": ["Imphal", "Thoubal", "Churachandpur", "Bishnupur", "Ukhrul", "Senapati", "Tamenglong", "Chandel", "Jiribam", "Moreh", "Lilong", "Mayang Imphal", "Moirang", "Kakching", "Lamlai", "Sekmai", "Wangjing", "Kakching Khunou", "Lamsang", "Oinam"],
  "Meghalaya": ["Shillong", "Tura", "Nongpoh", "Jowai", "Baghmara", "Williamnagar", "Resubelpara", "Khliehriat", "Mairang", "Nongstoin", "Mawkyrwat", "Ampati", "Dadenggre", "Mendipathar", "Mahendraganj", "Dalu", "Rongjeng", "Songsak", "Rongara", "Gasuapara"],
  "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip", "Kolasib", "Lawngtlai", "Mamit", "Saitual", "Khawzawl", "Hnahthial", "Siaha", "Thenzawl", "Biate", "Phullen", "Reiek", "Darlawn", "Vairengte", "Bairabi", "Sairang", "Tlabung"],
  "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha", "Zunheboto", "Phek", "Kiphire", "Longleng", "Peren", "Medziphema", "Chumukedima", "Pfutsero", "Meluri", "Tuli", "Tseminyu", "Bhandari", "Tizit", "Aboi", "Mon"],
  "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore", "Bhadrak", "Baripada", "Jharsuguda", "Bargarh", "Bhuban", "Dhenkanal", "Jajpur", "Jeypore", "Kendrapara", "Koraput", "Paradip", "Phulbani", "Rayagada"],
  "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Moga", "Muktsar", "Fatehgarh Sahib", "Gurdaspur", "Hoshiarpur", "Kapurthala", "Nawanshahr", "Rupnagar", "Sangrur", "Barnala", "Fazilka", "Ferozepur", "Malerkotla", "Pathankot", "Phagwara"],
  "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Bharatpur", "Bhilwara", "Pali", "Tonk", "Alwar", "Banswara", "Baran", "Barmer", "Bundi", "Chittorgarh", "Dausa", "Dholpur", "Hanumangarh", "Jaisalmer"],
  "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan", "Rangpo", "Singtam", "Jorethang", "Ravangla", "Pelling", "Lachen", "Lachung", "Yuksom", "Rumtek", "Rongli", "Rhenock", "Soreng", "Melli", "Majitar", "Ranipool", "Tadong"],
  "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli", "Tirunelveli", "Tiruppur", "Erode", "Vellore", "Thoothukudi", "Dindigul", "Thanjavur", "Tiruvannamalai", "Kanchipuram", "Nagercoil", "Kumbakonam", "Cuddalore", "Hosur", "Karaikudi", "Neyveli"],
  "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam", "Mahbubnagar", "Nalgonda", "Siddipet", "Suryapet", "Adilabad", "Jagtial", "Mancherial", "Medak", "Narayanpet", "Peddapalli", "Sangareddy", "Vikarabad", "Wanaparthy", "Yadadri"],
  "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailasahar", "Belonia", "Khowai", "Teliamura", "Ambassa", "Sabroom", "Kamalpur", "Amarpur", "Bishalgarh", "Jogendranagar", "Kumarghat", "Melaghar", "Ranirbazar", "Sonamura", "Udaipur", "Bishramganj", "Jampuijala"],
  "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Noida", "Ghaziabad", "Meerut", "Allahabad", "Bareilly", "Aligarh", "Moradabad", "Gorakhpur", "Saharanpur", "Jhansi", "Muzaffarnagar", "Mathura", "Firozabad", "Ayodhya", "Rampur", "Shahjahanpur"],
  "Uttarakhand": ["Dehradun", "Haridwar", "Haldwani", "Rudrapur", "Roorkee", "Kashipur", "Rishikesh", "Kotdwara", "Ramnagar", "Pithoragarh", "Almora", "Bageshwar", "Champawat", "Didihat", "Gopeshwar", "Joshimath", "Karanprayag", "Mussoorie", "Nainital", "Pauri"],
  "West Bengal": ["Kolkata", "Asansol", "Siliguri", "Durgapur", "Howrah", "Bardhaman", "Malda", "Baharampur", "Habra", "Kharagpur", "Alipurduar", "Balurghat", "Bankura", "Cooch Behar", "Darjeeling", "Jalpaiguri", "Krishnanagar", "Midnapore", "Raiganj", "Suri"],
  "Andaman and Nicobar Islands": ["Port Blair", "Diglipur", "Mayabunder", "Rangat", "Hut Bay", "Car Nicobar", "Campbell Bay", "Havelock", "Neil Island", "Long Island", "Baratang", "Wandoor", "Bambooflat", "Ferrargunj", "Prothrapur", "Chouldari", "Garacharma", "Junglighat", "Mannarghat", "Tusnabad"],
  "Chandigarh": ["Chandigarh", "Sector 1", "Sector 2", "Sector 3", "Sector 4", "Sector 5", "Sector 6", "Sector 7", "Sector 8", "Sector 9", "Sector 10", "Sector 11", "Sector 12", "Sector 13", "Sector 14", "Sector 15", "Sector 16", "Sector 17", "Sector 18", "Sector 19"],
  "Dadra and Nagar Haveli and Daman and Diu": ["Silvassa", "Daman", "Diu", "Amli", "Kachigam", "Dadra", "Naroli", "Masat", "Rakholi", "Samarvarni", "Khanvel", "Galonda", "Kadai", "Kherdi", "Khadoli", "Piparia", "Vapi", "Varkund", "Vasona", "Vatva"],
  "Delhi": ["New Delhi", "Dwarka", "Rohini", "Pitampura", "Saket", "Laxmi Nagar", "Mayur Vihar", "Vasant Kunj", "Hauz Khas", "Defence Colony", "Greater Kailash", "Rajouri Garden", "Janakpuri", "Paschim Vihar", "Patel Nagar", "Karol Bagh", "Connaught Place", "Chandni Chowk", "Shahdara", "Seelampur"],
  "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Udhampur", "Kathua", "Rajouri", "Poonch", "Doda", "Kishtwar", "Ramban", "Reasi", "Samba", "Shopian", "Kulgam", "Pulwama", "Budgam", "Ganderbal", "Bandipora", "Kupwara"],
  "Ladakh": ["Leh", "Kargil", "Diskit", "Nubra", "Padum", "Nyoma", "Durbuk", "Khaltsi", "Turtuk", "Hundar", "Panamik", "Sumur", "Tegar", "Chushul", "Dah", "Hanle", "Nyoma", "Thoise", "Turtuk", "Wakha"],
  "Lakshadweep": ["Kavaratti", "Agatti", "Amini", "Andrott", "Kalpeni", "Kadmat", "Kiltan", "Chetlat", "Bitra", "Amini", "Kadmat", "Kalpeni", "Kiltan", "Minicoy", "Andrott", "Agatti", "Bangaram", "Suheli", "Valiyakara", "Thinnakara"],
  "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam", "Ozhukarai", "Villianur", "Bahour", "Nettapakkam", "Mannadipet", "Ariyankuppam", "Embalam", "Kurumbapet", "Muthialpet", "Nellithope", "Orleanpet", "Reddiarpalayam", "Thirubuvanai", "Uzhavarkarai", "Vadhanur", "Veerampattinam"]
}


# Other dropdown options
fuel_types = ["Petrol", "Diesel", "CNG", "Electric", "Hybrid"]
transmission_types = ["Manual", "Automatic", "AMT", "CVT", "DCT"]
ownership_types = ["First", "Second", "Third", "Fourth"]
variants = ["LXI", "VXI", "ZXI", "ZXI+", "AMT", "Diesel", "Petrol"]
extra_features = [
    "Sunroof",
    "Rear Camera",
    "Navigation",
    "Alloy Wheels",
    "Touch Screen",
    "Airbags",
    "ABS",
    "Cruise Control",
    "Leather Seats",
    "Climate Control"
]

def get_models_for_maker(maker):
    """Get list of models for a given car maker"""
    return models.get(maker, [])

def get_cities_for_state(state):
    """Get list of cities for a given state"""
    return locations.get(state, []) 
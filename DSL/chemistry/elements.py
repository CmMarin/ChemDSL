"""
DSL/chemistry/elements.py

Provides definitions and data for chemical elements.
"""

# A more complete periodic table dictionary
ELEMENTS = {
    'H': {
        'name': 'Hydrogen',
        'atomic_weight': 1.008,
        'state': 'Gas',
        'group': 'Nonmetal',
        'electronegativity': 2.20,
        'common_compounds': ['H2O', 'HCl', 'H2SO4'],
        'common_reactions': ['2H2 + O2 -> 2H2O', 'H2 + Cl2 -> 2HCl']
    },
    'He': {
        'name': 'Helium',
        'atomic_weight': 4.0026,
        'state': 'Gas',
        'group': 'Noble Gas',
        'electronegativity': None,  # Noble gases have no electronegativity
        'common_compounds': [],  # Noble gases rarely form compounds
        'common_reactions': []
    },
    'Li': {
        'name': 'Lithium',
        'atomic_weight': 6.94,
        'state': 'Solid',
        'group': 'Alkali Metal',
        'electronegativity': 0.98,
        'common_compounds': ['Li2O', 'LiCl', 'LiOH'],
        'common_reactions': ['4Li + O2 -> 2Li2O', '2Li + 2H2O -> 2LiOH + H2']
    },
    'Be': {
        'name': 'Beryllium',
        'atomic_weight': 9.0122,
        'state': 'Solid',
        'group': 'Alkaline Earth Metal',
        'electronegativity': 1.57,
        'common_compounds': ['BeO', 'BeCl2'],
        'common_reactions': ['2Be + O2 -> 2BeO']
    },
    'B': {
        'name': 'Boron',
        'atomic_weight': 10.81,
        'state': 'Solid',
        'group': 'Metalloid',
        'electronegativity': 2.04,
        'common_compounds': ['B2O3', 'H3BO3'],
        'common_reactions': ['4B + 3O2 -> 2B2O3']
    },
    'C': {
        'name': 'Carbon',
        'atomic_weight': 12.011,
        'state': 'Solid',
        'group': 'Nonmetal',
        'electronegativity': 2.55,
        'common_compounds': ['CO2', 'CH4', 'C6H12O6'],
        'common_reactions': ['C + O2 -> CO2', 'CH4 + 2O2 -> CO2 + 2H2O']
    },
    'N': {
        'name': 'Nitrogen',
        'atomic_weight': 14.007,
        'state': 'Gas',
        'group': 'Nonmetal',
        'electronegativity': 3.04,
        'common_compounds': ['NH3', 'NO2', 'HNO3'],
        'common_reactions': ['N2 + 3H2 -> 2NH3']
    },
    'O': {
        'name': 'Oxygen',
        'atomic_weight': 15.999,
        'state': 'Gas',
        'group': 'Nonmetal',
        'electronegativity': 3.44,
        'common_compounds': ['H2O', 'CO2', 'O3'],
        'common_reactions': ['2H2 + O2 -> 2H2O', 'C + O2 -> CO2']
    },
    'F': {
        'name': 'Fluorine',
        'atomic_weight': 18.998,
        'state': 'Gas',
        'group': 'Halogen',
        'electronegativity': 3.98,
        'common_compounds': ['HF', 'NaF'],
        'common_reactions': ['H2 + F2 -> 2HF']
    },
    'Ne': {
        'name': 'Neon',
        'atomic_weight': 20.180,
        'state': 'Gas',
        'group': 'Noble Gas',
        'electronegativity': None,
        'common_compounds': [],
        'common_reactions': []
    },
    'Na': {
        'name': 'Sodium',
        'atomic_weight': 22.990,
        'state': 'Solid',
        'group': 'Alkali Metal',
        'electronegativity': 0.93,
        'common_compounds': ['NaCl', 'NaOH', 'Na2CO3'],
        'common_reactions': ['2Na + Cl2 -> 2NaCl', '2Na + 2H2O -> 2NaOH + H2']
    },
    'Mg': {
        'name': 'Magnesium',
        'atomic_weight': 24.305,
        'state': 'Solid',
        'group': 'Alkaline Earth Metal',
        'electronegativity': 1.31,
        'common_compounds': ['MgO', 'MgCl2'],
        'common_reactions': ['2Mg + O2 -> 2MgO']
    },
    'Al': {
        'name': 'Aluminum',
        'atomic_weight': 26.982,
        'state': 'Solid',
        'group': 'Post-Transition Metal',
        'electronegativity': 1.61,
        'common_compounds': ['Al2O3', 'AlCl3'],
        'common_reactions': ['4Al + 3O2 -> 2Al2O3']
    },
    'Si': {
        'name': 'Silicon',
        'atomic_weight': 28.085,
        'state': 'Solid',
        'group': 'Metalloid',
        'electronegativity': 1.90,
        'common_compounds': ['SiO2', 'SiCl4'],
        'common_reactions': ['Si + O2 -> SiO2']
    },
    'P': {
        'name': 'Phosphorus',
        'atomic_weight': 30.974,
        'state': 'Solid',
        'group': 'Nonmetal',
        'electronegativity': 2.19,
        'common_compounds': ['P2O5', 'H3PO4'],
        'common_reactions': ['4P + 5O2 -> 2P2O5']
    },
    'S': {
        'name': 'Sulfur',
        'atomic_weight': 32.06,
        'state': 'Solid',
        'group': 'Nonmetal',
        'electronegativity': 2.58,
        'common_compounds': ['SO2', 'H2SO4'],
        'common_reactions': ['S + O2 -> SO2']
    },
    'Cl': {
        'name': 'Chlorine',
        'atomic_weight': 35.45,
        'state': 'Gas',
        'group': 'Halogen',
        'electronegativity': 3.16,
        'common_compounds': ['HCl', 'NaCl'],
        'common_reactions': ['H2 + Cl2 -> 2HCl']
    },
    'Ar': {
        'name': 'Argon',
        'atomic_weight': 39.948,
        'state': 'Gas',
        'group': 'Noble Gas',
        'electronegativity': None,
        'common_compounds': [],
        'common_reactions': []
    },
    'K': {
        'name': 'Potassium',
        'atomic_weight': 39.098,
        'state': 'Solid',
        'group': 'Alkali Metal',
        'electronegativity': 0.82,
        'common_compounds': ['KCl', 'KOH'],
        'common_reactions': ['2K + Cl2 -> 2KCl']
    },
    'Ca': {
        'name': 'Calcium',
        'atomic_weight': 40.078,
        'state': 'Solid',
        'group': 'Alkaline Earth Metal',
        'electronegativity': 1.00,
        'common_compounds': ['CaO', 'CaCO3'],
        'common_reactions': ['2Ca + O2 -> 2CaO']
    },
    'Fe': {
        'name': 'Iron',
        'atomic_weight': 55.845,
        'state': 'Solid',
        'group': 'Transition Metal',
        'electronegativity': 1.83,
        'common_compounds': ['Fe2O3', 'FeCl3'],
        'common_reactions': ['4Fe + 3O2 -> 2Fe2O3']
    },
    'Cu': {
        'name': 'Copper',
        'atomic_weight': 63.546,
        'state': 'Solid',
        'group': 'Transition Metal',
        'electronegativity': 1.90,
        'common_compounds': ['CuO', 'CuSO4'],
        'common_reactions': ['2Cu + O2 -> 2CuO']
    },
    'Zn': {
        'name': 'Zinc',
        'atomic_weight': 65.38,
        'state': 'Solid',
        'group': 'Transition Metal',
        'electronegativity': 1.65,
        'common_compounds': ['ZnO', 'ZnCl2'],
        'common_reactions': ['2Zn + O2 -> 2ZnO']
    }
}

def get_element(symbol):
    """
    Get element data for the given symbol.
    Raises ValueError if the element symbol is unknown.
    """
    if symbol not in ELEMENTS:
        raise ValueError(f"Unknown element symbol: {symbol}")
    return ELEMENTS[symbol]


# Dictionary of common chemical compounds with detailed information
COMPOUNDS = {
    'H2O': {
        'name': 'Water',
        'formula': 'H2O',
        'molar_mass': 18.015,
        'state': 'Liquid',
        'classification': 'Inorganic',
        'density': 1.0,  # g/cm³ at 4°C
        'melting_point': 0.0,  # °C
        'boiling_point': 100.0,  # °C
        'solubility': 'N/A (self)',
        'acidity': 7.0,  # pH
        'common_uses': ['Solvent', 'Cooling', 'Drinking', 'Agriculture'],
        'hazards': ['None (pure form)'],
        'production_methods': ['Natural occurrence', 'Hydrogen combustion: 2H₂ + O₂ → 2H₂O'],
        'reactions': ['Hydrolysis', 'Acid-base reactions', 'Hydration']
    },
    'CO2': {
        'name': 'Carbon Dioxide',
        'formula': 'CO2',
        'molar_mass': 44.009,
        'state': 'Gas',
        'classification': 'Inorganic',
        'density': 1.98,  # g/L at 25°C
        'melting_point': -78.5,  # °C (sublimates)
        'boiling_point': -56.6,  # °C (at 5.2 atm)
        'solubility': '1.45 g/L in water at 25°C',
        'acidity': 'Forms carbonic acid (H₂CO₃) in water',
        'common_uses': ['Carbonated beverages', 'Fire extinguishers', 'Refrigerant', 'Plant photosynthesis'],
        'hazards': ['Asphyxiant at high concentrations', 'Greenhouse gas'],
        'production_methods': ['Combustion of carbon compounds', 'Fermentation', 'Thermal decomposition of carbonates'],
        'reactions': ['CO₂ + H₂O ⇌ H₂CO₃', 'Photosynthesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂']
    },
    'NaCl': {
        'name': 'Sodium Chloride (Table Salt)',
        'formula': 'NaCl',
        'molar_mass': 58.44,
        'state': 'Solid',
        'classification': 'Ionic salt',
        'density': 2.16,  # g/cm³
        'melting_point': 801,  # °C
        'boiling_point': 1413,  # °C
        'solubility': '360 g/L in water at 20°C',
        'acidity': 'Neutral (pH 7)',
        'common_uses': ['Food preservative', 'Seasoning', 'De-icing', 'Chemical production'],
        'hazards': ['Hypertension at excessive intake'],
        'production_methods': ['Seawater evaporation', 'Rock salt mining', 'Reaction: 2Na + Cl₂ → 2NaCl'],
        'reactions': ['Electrolysis: 2NaCl + 2H₂O → 2NaOH + H₂ + Cl₂']
    },
    'NH3': {
        'name': 'Ammonia',
        'formula': 'NH3',
        'molar_mass': 17.031,
        'state': 'Gas',
        'classification': 'Inorganic',
        'density': 0.769,  # g/L at 0°C
        'melting_point': -77.73,  # °C
        'boiling_point': -33.34,  # °C
        'solubility': 'Highly soluble in water (31% w/w at 25°C)',
        'acidity': 'Basic (pH ~11 in solution)',
        'common_uses': ['Fertilizer production', 'Cleaning products', 'Refrigerant', 'Chemical synthesis'],
        'hazards': ['Toxic', 'Corrosive to respiratory tract', 'Flammable'],
        'production_methods': ['Haber process: N₂ + 3H₂ → 2NH₃'],
        'reactions': ['NH₃ + H₂O → NH₄OH', '4NH₃ + 5O₂ → 4NO + 6H₂O']
    },
    'H2SO4': {
        'name': 'Sulfuric Acid',
        'formula': 'H2SO4',
        'molar_mass': 98.079,
        'state': 'Liquid',
        'classification': 'Strong mineral acid',
        'density': 1.84,  # g/cm³
        'melting_point': 10.31,  # °C
        'boiling_point': 337,  # °C
        'solubility': 'Miscible with water',
        'acidity': 'Highly acidic (pH < 1)',
        'common_uses': ['Battery acid', 'Fertilizer production', 'Mineral processing', 'Chemical synthesis'],
        'hazards': ['Highly corrosive', 'Causes severe burns', 'Dehydrating agent'],
        'production_methods': ['Contact process: S + O₂ → SO₂, 2SO₂ + O₂ → 2SO₃, SO₃ + H₂O → H₂SO₄'],
        'reactions': ['Dehydration', 'Acid-base reactions', 'Oxidation reactions']
    },
    'C6H12O6': {
        'name': 'Glucose',
        'formula': 'C6H12O6',
        'molar_mass': 180.156,
        'state': 'Solid',
        'classification': 'Carbohydrate (monosaccharide)',
        'density': 1.54,  # g/cm³
        'melting_point': 146,  # °C
        'boiling_point': 'Decomposes',
        'solubility': '900 g/L in water at 25°C',
        'acidity': 'Slightly acidic',
        'common_uses': ['Energy source in living organisms', 'Food additive', 'Medical applications', 'Fermentation substrate'],
        'hazards': ['None significant'],
        'production_methods': ['Photosynthesis', 'Hydrolysis of starch', 'Industrial enzymatic processes'],
        'reactions': ['Fermentation: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 'Cellular respiration: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energy']
    },
    'HCl': {
        'name': 'Hydrochloric Acid',
        'formula': 'HCl',
        'molar_mass': 36.461,
        'state': 'Gas (anhydrous), Liquid (in solution)',
        'classification': 'Strong mineral acid',
        'density': '1.2 g/cm³ (37% solution)',
        'melting_point': -27.32,  # °C (anhydrous)
        'boiling_point': -85.05,  # °C (anhydrous)
        'solubility': 'Very soluble in water',
        'acidity': 'Highly acidic (pH < 1)',
        'common_uses': ['Chemical manufacturing', 'Metal cleaning', 'Food processing', 'Gastric acid in digestion'],
        'hazards': ['Corrosive', 'Respiratory irritant'],
        'production_methods': ['Salt and sulfuric acid: NaCl + H₂SO₄ → NaHSO₄ + HCl', 'Direct synthesis: H₂ + Cl₂ → 2HCl'],
        'reactions': ['Acid-base neutralization', 'Metal dissolution', 'Chloride salt formation']
    },
    'CH4': {
        'name': 'Methane',
        'formula': 'CH4',
        'molar_mass': 16.043,
        'state': 'Gas',
        'classification': 'Alkane (hydrocarbon)',
        'density': 0.657,  # g/L at 25°C
        'melting_point': -182.5,  # °C
        'boiling_point': -161.5,  # °C
        'solubility': 'Slightly soluble in water (22.7 mg/L)',
        'acidity': 'Neutral',
        'common_uses': ['Natural gas fuel', 'Chemical synthesis', 'Hydrogen production'],
        'hazards': ['Highly flammable', 'Asphyxiant', 'Greenhouse gas'],
        'production_methods': ['Natural gas extraction', 'Anaerobic digestion', 'Methanogenesis'],
        'reactions': ['Combustion: CH₄ + 2O₂ → CO₂ + 2H₂O', 'Steam reforming: CH₄ + H₂O → CO + 3H₂']
    },
    'NaOH': {
        'name': 'Sodium Hydroxide (Caustic Soda)',
        'formula': 'NaOH',
        'molar_mass': 40.00,
        'state': 'Solid',
        'classification': 'Strong base',
        'density': 2.13,  # g/cm³
        'melting_point': 318,  # °C
        'boiling_point': 1388,  # °C
        'solubility': '1110 g/L in water at 20°C',
        'acidity': 'Highly basic (pH ~14)',
        'common_uses': ['Soap making', 'Paper production', 'Drain cleaner', 'Chemical manufacturing'],
        'hazards': ['Corrosive', 'Causes severe burns', 'Reacts violently with acids'],
        'production_methods': ['Chloralkali process: 2NaCl + 2H₂O → 2NaOH + Cl₂ + H₂'],
        'reactions': ['Acid neutralization', 'Saponification', 'Aluminum dissolution: 2Al + 2NaOH + 6H₂O → 2Na[Al(OH)₄] + 3H₂']
    },
    'C2H5OH': {
        'name': 'Ethanol (Ethyl Alcohol)',
        'formula': 'C2H5OH',
        'molar_mass': 46.068,
        'state': 'Liquid',
        'classification': 'Alcohol',
        'density': 0.789,  # g/cm³ at 20°C
        'melting_point': -114.1,  # °C
        'boiling_point': 78.37,  # °C
        'solubility': 'Miscible with water',
        'acidity': 'Slightly acidic (pKa ~15.9)',
        'common_uses': ['Alcoholic beverages', 'Solvent', 'Antiseptic', 'Fuel'],
        'hazards': ['Flammable', 'Intoxicant', 'Toxic in large quantities'],
        'production_methods': ['Fermentation of sugars: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 'Hydration of ethylene: C₂H₄ + H₂O → C₂H₅OH'],
        'reactions': ['Combustion: C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O', 'Oxidation: C₂H₅OH + O₂ → CH₃COOH + H₂O']
    },
    'CaCO3': {
        'name': 'Calcium Carbonate',
        'formula': 'CaCO3',
        'molar_mass': 100.087,
        'state': 'Solid',
        'classification': 'Ionic carbonate salt',
        'density': 2.71,  # g/cm³
        'melting_point': 'Decomposes at 825°C',
        'boiling_point': 'Decomposes',
        'solubility': 'Low in water (0.013 g/L at 25°C)',
        'acidity': 'Basic (pH ~9 in solution)',
        'common_uses': ['Antacid', 'Construction material (limestone)', 'Dietary supplement', 'Paper filler'],
        'hazards': ['Low hazard'],
        'production_methods': ['Mining (limestone, marble)', 'Precipitation: Ca²⁺ + CO₃²⁻ → CaCO₃'],
        'reactions': ['Thermal decomposition: CaCO₃ → CaO + CO₂', 'Acid reaction: CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂']
    },
    'O3': {
        'name': 'Ozone',
        'formula': 'O3',
        'molar_mass': 47.997,
        'state': 'Gas',
        'classification': 'Allotrope of oxygen',
        'density': 2.144,  # g/L at 0°C
        'melting_point': -192.2,  # °C
        'boiling_point': -112,  # °C
        'solubility': '0.105 g/L in water at 0°C',
        'acidity': 'N/A',
        'common_uses': ['Water purification', 'Air disinfection', 'Industrial oxidant'],
        'hazards': ['Strong oxidizer', 'Respiratory irritant', 'Can damage lungs at high concentrations'],
        'production_methods': ['Electrical discharge in oxygen: 3O₂ → 2O₃', 'UV radiation of oxygen'],
        'reactions': ['Decomposition: 2O₃ → 3O₂', 'Oxidation reactions']
    },
    'H2O2': {
        'name': 'Hydrogen Peroxide',
        'formula': 'H2O2',
        'molar_mass': 34.015,
        'state': 'Liquid',
        'classification': 'Peroxide',
        'density': 1.45,  # g/cm³ (pure)
        'melting_point': -0.43,  # °C
        'boiling_point': 150.2,  # °C
        'solubility': 'Miscible with water',
        'acidity': 'Weakly acidic (pKa 11.6)',
        'common_uses': ['Bleaching agent', 'Disinfectant', 'Propellant', 'Chemical synthesis'],
        'hazards': ['Strong oxidizer', 'Corrosive at high concentrations', 'Decomposes explosively when heated'],
        'production_methods': ['Anthraquinone process', 'Electrochemical process: 2H₂O → H₂O₂ + H₂'],
        'reactions': ['Decomposition: 2H₂O₂ → 2H₂O + O₂', 'Oxidation reactions']
    },
    'C6H6': {
        'name': 'Benzene',
        'formula': 'C6H6',
        'molar_mass': 78.114,
        'state': 'Liquid',
        'classification': 'Aromatic hydrocarbon',
        'density': 0.879,  # g/cm³ at 20°C
        'melting_point': 5.53,  # °C
        'boiling_point': 80.1,  # °C
        'solubility': 'Low in water (1.8 g/L at 25°C), miscible with organic solvents',
        'acidity': 'Neutral',
        'common_uses': ['Chemical synthesis', 'Solvent', 'Gasoline component'],
        'hazards': ['Carcinogenic', 'Flammable', 'Toxic'],
        'production_methods': ['Catalytic reforming of petroleum', 'Toluene hydrodealkylation'],
        'reactions': ['Electrophilic aromatic substitution', 'Combustion', 'Addition reactions']
    }
}

def get_compound(formula):
    """
    Get compound data for the given formula.
    Raises ValueError if the compound formula is unknown.
    """
    if formula not in COMPOUNDS:
        raise ValueError(f"Unknown compound formula: {formula}")
    return COMPOUNDS[formula]
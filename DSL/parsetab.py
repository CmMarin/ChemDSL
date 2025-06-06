
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ACID_BASE ALGEBRAIC ANALYZE AND AQUEOUS ARROW ASSIGN BALANCE CARET CATALYST COMBUSTION COMMA COMPOUND DECOMPOSITION DOUBLE_REPLACEMENT ELEMENT ELEMENT_SYMBOL EMPIRICAL_FORMULA ENTHALPY ENTROPY EQUALS EQUILIBRIUM FLOAT FOR GAS GAS_FORMATION GIBBS_ENERGY HALF_REACTION HEAT IDENTIFIER IF INFO INTEGER LBRACE LBRACKET LIMITING_REAGENT LIQUID LPAREN MOLARITY MOLAR_MASS MOLECULAR_FORMULA NEGATIVE NORMALITY OF OR OXIDATION_NUMBER OXIDATION_STATES PERCENT_YIELD PH PLUS POSITIVE PRECIPITATION PREDICT PRESSURE QUERY RBRACE RBRACKET REACTION REACTION_TYPE REDOX RESONANCE_ARROW REVERSIBLE_ARROW RPAREN SEMICOLON SINGLE_REPLACEMENT SOLID STRING TEMPERATURE TIME WITH YIELDprogram : statement_liststatement_list : statement SEMICOLON statement_list\n                     | statement SEMICOLONstatement : balance_statement\n                 | predict_statement\n                 | analyze_statement\n                 | reaction_type_statement\n                 | thermodynamic_statement\n                 | chemical_analysis_statementbalance_statement : BALANCE reaction_exprpredict_statement : PREDICT reaction_expr\n                         | PREDICT reaction_expr IF condition\n                         | PREDICT reactants_expr\n                         | PREDICT reactants_expr IF conditioncondition : condition AND condition\n                 | condition OR condition\n                 | CATALYST LPAREN ELEMENT_SYMBOL RPAREN\n                 | TEMPERATURE LPAREN INTEGER IDENTIFIER RPAREN\n                 | PRESSURE LPAREN INTEGER IDENTIFIER RPARENanalyze_statement : ANALYZE molecule\n                         | ANALYZE molecule FOR IDENTIFIERreaction_type_statement : COMBUSTION\n                               | DECOMPOSITION\n                               | SINGLE_REPLACEMENT\n                               | DOUBLE_REPLACEMENT\n                               | ACID_BASE\n                               | PRECIPITATION\n                               | GAS_FORMATION\n                               | COMBUSTION OF molecule\n                               | DECOMPOSITION OF molecule\n                               | SINGLE_REPLACEMENT OF molecule\n                               | DOUBLE_REPLACEMENT OF molecule\n                               | ACID_BASE OF molecule\n                               | PRECIPITATION OF molecule\n                               | GAS_FORMATION OF moleculethermodynamic_statement : ENTHALPY OF reaction_expr\n                               | ENTROPY OF reaction_expr\n                               | GIBBS_ENERGY OF reaction_expr\n                               | EQUILIBRIUM OF reaction_expr\n                               | ENTHALPY INFO reaction_expr\n                               | ENTROPY INFO reaction_expr\n                               | GIBBS_ENERGY INFO reaction_expr\n                               | EQUILIBRIUM INFO reaction_exprchemical_analysis_statement : OXIDATION_STATES OF molecule\n                                   | LIMITING_REAGENT OF reaction_expr\n                                   | PERCENT_YIELD OF reaction_expr\n                                   | EMPIRICAL_FORMULA OF molecule\n                                   | MOLECULAR_FORMULA OF molecule\n                                   | MOLAR_MASS OF moleculereaction_expr : reactants_expr ARROW products_exprreactants_expr : chemical_term_listproducts_expr : chemical_term_listchemical_term_list : chemical_term PLUS chemical_term_list\n                          | chemical_termchemical_term : INTEGER molecule\n                     | moleculemolecule : molecule_part molecule\n                | molecule_partmolecule_part : element_group\n                     | LPAREN molecule RPAREN INTEGERelement_group : ELEMENT_SYMBOL INTEGER\n                     | ELEMENT_SYMBOL'
    
_lr_action_items = {'BALANCE':([0,30,],[10,10,]),'PREDICT':([0,30,],[11,11,]),'ANALYZE':([0,30,],[12,12,]),'COMBUSTION':([0,30,],[13,13,]),'DECOMPOSITION':([0,30,],[14,14,]),'SINGLE_REPLACEMENT':([0,30,],[15,15,]),'DOUBLE_REPLACEMENT':([0,30,],[16,16,]),'ACID_BASE':([0,30,],[17,17,]),'PRECIPITATION':([0,30,],[18,18,]),'GAS_FORMATION':([0,30,],[19,19,]),'ENTHALPY':([0,30,],[20,20,]),'ENTROPY':([0,30,],[21,21,]),'GIBBS_ENERGY':([0,30,],[22,22,]),'EQUILIBRIUM':([0,30,],[23,23,]),'OXIDATION_STATES':([0,30,],[24,24,]),'LIMITING_REAGENT':([0,30,],[25,25,]),'PERCENT_YIELD':([0,30,],[26,26,]),'EMPIRICAL_FORMULA':([0,30,],[27,27,]),'MOLECULAR_FORMULA':([0,30,],[28,28,]),'MOLAR_MASS':([0,30,],[29,29,]),'$end':([1,2,30,65,],[0,-1,-3,-2,]),'SEMICOLON':([3,4,5,6,7,8,9,13,14,15,16,17,18,19,31,33,34,36,37,38,40,41,42,43,68,69,71,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,104,105,106,112,113,117,120,121,],[30,-4,-5,-6,-7,-8,-9,-22,-23,-24,-25,-26,-27,-28,-10,-51,-54,-56,-58,-59,-62,-11,-13,-20,-55,-57,-61,-29,-30,-31,-32,-33,-34,-35,-36,-40,-37,-41,-38,-42,-39,-43,-44,-45,-46,-47,-48,-49,-50,-52,-53,-12,-14,-21,-60,-15,-16,-17,-18,-19,]),'INTEGER':([10,11,40,51,52,53,54,55,56,57,58,60,61,66,67,99,110,111,],[35,35,71,35,35,35,35,35,35,35,35,35,35,35,35,106,115,116,]),'LPAREN':([10,11,12,35,37,38,39,40,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,71,101,102,103,106,],[39,39,39,39,39,-59,39,-62,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,-61,109,110,111,-60,]),'ELEMENT_SYMBOL':([10,11,12,35,37,38,39,40,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,71,106,109,],[40,40,40,40,40,-59,40,-62,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,-61,-60,114,]),'OF':([13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,],[44,45,46,47,48,49,50,51,53,55,57,59,60,61,62,63,64,]),'INFO':([20,21,22,23,],[52,54,56,58,]),'ARROW':([32,33,34,36,37,38,40,42,68,69,71,98,106,],[66,-51,-54,-56,-58,-59,-62,66,-55,-57,-61,-53,-60,]),'IF':([33,34,36,37,38,40,41,42,68,69,71,96,97,98,106,],[-51,-54,-56,-58,-59,-62,72,73,-55,-57,-61,-50,-52,-53,-60,]),'PLUS':([34,36,37,38,40,68,69,71,106,],[67,-56,-58,-59,-62,-55,-57,-61,-60,]),'FOR':([37,38,40,43,69,71,106,],[-58,-59,-62,74,-57,-61,-60,]),'RPAREN':([37,38,40,69,70,71,106,114,118,119,],[-58,-59,-62,-57,99,-61,-60,117,120,121,]),'CATALYST':([72,73,107,108,],[101,101,101,101,]),'TEMPERATURE':([72,73,107,108,],[102,102,102,102,]),'PRESSURE':([72,73,107,108,],[103,103,103,103,]),'IDENTIFIER':([74,115,116,],[105,118,119,]),'AND':([100,104,112,113,117,120,121,],[107,107,107,107,-17,-18,-19,]),'OR':([100,104,112,113,117,120,121,],[108,108,108,108,-17,-18,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statement_list':([0,30,],[2,65,]),'statement':([0,30,],[3,3,]),'balance_statement':([0,30,],[4,4,]),'predict_statement':([0,30,],[5,5,]),'analyze_statement':([0,30,],[6,6,]),'reaction_type_statement':([0,30,],[7,7,]),'thermodynamic_statement':([0,30,],[8,8,]),'chemical_analysis_statement':([0,30,],[9,9,]),'reaction_expr':([10,11,51,52,53,54,55,56,57,58,60,61,],[31,41,82,83,84,85,86,87,88,89,91,92,]),'reactants_expr':([10,11,51,52,53,54,55,56,57,58,60,61,],[32,42,32,32,32,32,32,32,32,32,32,32,]),'chemical_term_list':([10,11,51,52,53,54,55,56,57,58,60,61,66,67,],[33,33,33,33,33,33,33,33,33,33,33,33,97,98,]),'chemical_term':([10,11,51,52,53,54,55,56,57,58,60,61,66,67,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'molecule':([10,11,12,35,37,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,],[36,36,43,68,69,70,75,76,77,78,79,80,81,36,36,36,36,36,36,36,36,90,36,36,93,94,95,36,36,]),'molecule_part':([10,11,12,35,37,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'element_group':([10,11,12,35,37,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'products_expr':([66,],[96,]),'condition':([72,73,107,108,],[100,104,112,113,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',13),
  ('statement_list -> statement SEMICOLON statement_list','statement_list',3,'p_statement_list','parser.py',18),
  ('statement_list -> statement SEMICOLON','statement_list',2,'p_statement_list','parser.py',19),
  ('statement -> balance_statement','statement',1,'p_statement','parser.py',23),
  ('statement -> predict_statement','statement',1,'p_statement','parser.py',24),
  ('statement -> analyze_statement','statement',1,'p_statement','parser.py',25),
  ('statement -> reaction_type_statement','statement',1,'p_statement','parser.py',26),
  ('statement -> thermodynamic_statement','statement',1,'p_statement','parser.py',27),
  ('statement -> chemical_analysis_statement','statement',1,'p_statement','parser.py',28),
  ('balance_statement -> BALANCE reaction_expr','balance_statement',2,'p_balance_statement','parser.py',33),
  ('predict_statement -> PREDICT reaction_expr','predict_statement',2,'p_predict_statement','parser.py',38),
  ('predict_statement -> PREDICT reaction_expr IF condition','predict_statement',4,'p_predict_statement','parser.py',39),
  ('predict_statement -> PREDICT reactants_expr','predict_statement',2,'p_predict_statement','parser.py',40),
  ('predict_statement -> PREDICT reactants_expr IF condition','predict_statement',4,'p_predict_statement','parser.py',41),
  ('condition -> condition AND condition','condition',3,'p_condition','parser.py',74),
  ('condition -> condition OR condition','condition',3,'p_condition','parser.py',75),
  ('condition -> CATALYST LPAREN ELEMENT_SYMBOL RPAREN','condition',4,'p_condition','parser.py',76),
  ('condition -> TEMPERATURE LPAREN INTEGER IDENTIFIER RPAREN','condition',5,'p_condition','parser.py',77),
  ('condition -> PRESSURE LPAREN INTEGER IDENTIFIER RPAREN','condition',5,'p_condition','parser.py',78),
  ('analyze_statement -> ANALYZE molecule','analyze_statement',2,'p_analyze_statement','parser.py',99),
  ('analyze_statement -> ANALYZE molecule FOR IDENTIFIER','analyze_statement',4,'p_analyze_statement','parser.py',100),
  ('reaction_type_statement -> COMBUSTION','reaction_type_statement',1,'p_reaction_type_statement','parser.py',110),
  ('reaction_type_statement -> DECOMPOSITION','reaction_type_statement',1,'p_reaction_type_statement','parser.py',111),
  ('reaction_type_statement -> SINGLE_REPLACEMENT','reaction_type_statement',1,'p_reaction_type_statement','parser.py',112),
  ('reaction_type_statement -> DOUBLE_REPLACEMENT','reaction_type_statement',1,'p_reaction_type_statement','parser.py',113),
  ('reaction_type_statement -> ACID_BASE','reaction_type_statement',1,'p_reaction_type_statement','parser.py',114),
  ('reaction_type_statement -> PRECIPITATION','reaction_type_statement',1,'p_reaction_type_statement','parser.py',115),
  ('reaction_type_statement -> GAS_FORMATION','reaction_type_statement',1,'p_reaction_type_statement','parser.py',116),
  ('reaction_type_statement -> COMBUSTION OF molecule','reaction_type_statement',3,'p_reaction_type_statement','parser.py',117),
  ('reaction_type_statement -> DECOMPOSITION OF molecule','reaction_type_statement',3,'p_reaction_type_statement','parser.py',118),
  ('reaction_type_statement -> SINGLE_REPLACEMENT OF molecule','reaction_type_statement',3,'p_reaction_type_statement','parser.py',119),
  ('reaction_type_statement -> DOUBLE_REPLACEMENT OF molecule','reaction_type_statement',3,'p_reaction_type_statement','parser.py',120),
  ('reaction_type_statement -> ACID_BASE OF molecule','reaction_type_statement',3,'p_reaction_type_statement','parser.py',121),
  ('reaction_type_statement -> PRECIPITATION OF molecule','reaction_type_statement',3,'p_reaction_type_statement','parser.py',122),
  ('reaction_type_statement -> GAS_FORMATION OF molecule','reaction_type_statement',3,'p_reaction_type_statement','parser.py',123),
  ('thermodynamic_statement -> ENTHALPY OF reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',130),
  ('thermodynamic_statement -> ENTROPY OF reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',131),
  ('thermodynamic_statement -> GIBBS_ENERGY OF reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',132),
  ('thermodynamic_statement -> EQUILIBRIUM OF reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',133),
  ('thermodynamic_statement -> ENTHALPY INFO reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',134),
  ('thermodynamic_statement -> ENTROPY INFO reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',135),
  ('thermodynamic_statement -> GIBBS_ENERGY INFO reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',136),
  ('thermodynamic_statement -> EQUILIBRIUM INFO reaction_expr','thermodynamic_statement',3,'p_thermodynamic_statement','parser.py',137),
  ('chemical_analysis_statement -> OXIDATION_STATES OF molecule','chemical_analysis_statement',3,'p_chemical_analysis_statement','parser.py',145),
  ('chemical_analysis_statement -> LIMITING_REAGENT OF reaction_expr','chemical_analysis_statement',3,'p_chemical_analysis_statement','parser.py',146),
  ('chemical_analysis_statement -> PERCENT_YIELD OF reaction_expr','chemical_analysis_statement',3,'p_chemical_analysis_statement','parser.py',147),
  ('chemical_analysis_statement -> EMPIRICAL_FORMULA OF molecule','chemical_analysis_statement',3,'p_chemical_analysis_statement','parser.py',148),
  ('chemical_analysis_statement -> MOLECULAR_FORMULA OF molecule','chemical_analysis_statement',3,'p_chemical_analysis_statement','parser.py',149),
  ('chemical_analysis_statement -> MOLAR_MASS OF molecule','chemical_analysis_statement',3,'p_chemical_analysis_statement','parser.py',150),
  ('reaction_expr -> reactants_expr ARROW products_expr','reaction_expr',3,'p_reaction_expr','parser.py',154),
  ('reactants_expr -> chemical_term_list','reactants_expr',1,'p_reactants_expr','parser.py',158),
  ('products_expr -> chemical_term_list','products_expr',1,'p_products_expr','parser.py',162),
  ('chemical_term_list -> chemical_term PLUS chemical_term_list','chemical_term_list',3,'p_chemical_term_list','parser.py',166),
  ('chemical_term_list -> chemical_term','chemical_term_list',1,'p_chemical_term_list','parser.py',167),
  ('chemical_term -> INTEGER molecule','chemical_term',2,'p_chemical_term','parser.py',171),
  ('chemical_term -> molecule','chemical_term',1,'p_chemical_term','parser.py',172),
  ('molecule -> molecule_part molecule','molecule',2,'p_molecule','parser.py',181),
  ('molecule -> molecule_part','molecule',1,'p_molecule','parser.py',182),
  ('molecule_part -> element_group','molecule_part',1,'p_molecule_part','parser.py',191),
  ('molecule_part -> LPAREN molecule RPAREN INTEGER','molecule_part',4,'p_molecule_part','parser.py',192),
  ('element_group -> ELEMENT_SYMBOL INTEGER','element_group',2,'p_element_group','parser.py',205),
  ('element_group -> ELEMENT_SYMBOL','element_group',1,'p_element_group','parser.py',206),
]

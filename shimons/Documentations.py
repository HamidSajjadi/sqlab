Documentation = {"overview": {"title": "Overview",
                              "content": '<p>PDB<sub>GTGT</sub> is based on the automatic generation of testbeds '
                                         'using graph theory. '
                                         ' Figure 1 demonstrates the PDB<sub>GTGT</sub> use case diagram.</p>'
                                         '<p><img src="/static/sqlab/img/Figure1_PDBgtgt_use_case.jpg" alt="Figure 1: '
                                         'PDB_GTGT  use case diagram"/></p> '
                                         '<p>In the following, to address more details about PDB<sub>GTGT</sub>, '
                                         'we will introduce the process of evaluating pattern detection methods in '
                                         'our proposed benchmark.</p> '
                                         '<p><img src="/static/sqlab/img/Figure2_evaluation_PDBgtgt.png" alt="Figure '
                                         '2: The process of evaluation in PDB_GTGT"/></p> '
                              },
                 "upload": {"title": "Upload Section",
                            "content": '<p>In this section, a set of initial settings will be saved. Also, some inputs are taken from the user and are stored in the database.</p><p>Inputs are the coded algorithm of the detection method in Java (jar file) and also the user desired patterns for inserting into the testbed.</p><ul><li>Detection methods to be evaluated in PDB<sub>GTGT</sub>, should be able to receive input in the form of a Java code or a class diagram.</li><li>To facilitate the comparison and ranking of methods, a predefined list of patterns is suggested to the user to be used in the code.</li><li>If the user does not select a pattern in the list, this means that the input method is unable to mine that pattern.</li></ul><p>Note 1: The user may upload some library jar files along with the detection code. Therefore, he/she should specify the main source among the uploaded files.</p><p>Note 2: To define new patterns in PDB<sub>GTGT</sub>, a specific grammar is developed which is derived from the specification of the Java and C languages and covers the object-oriented features (Click here to download the grammar file). This grammar has an XML structure and allows users to define the requirements of their patterns using a set of tags. In Table 1, these tags are listed (Click here to download the Singleton design pattern grammar as an example).</p><p>Note 3: Users should test their pattern definition files by the application before uploading. &nbsp;</p><table><tbody><tr><td>Tag</td><td>Fields</td><td>Definition</td></tr><tr><td>&lt;class&gt;&hellip;&lt;/class&gt;</td><td>modifiers, name, role, opt, isMandatory<sup>*</sup></td><td>Define the structure of a class</td></tr><tr><td>&lt;interface&gt;&hellip;&lt;/interface&gt;</td><td>modifiers, name, role, opt, isMandatory</td><td>Define the structure of an interface</td></tr><tr><td>&lt;attribute&gt;&hellip;&lt;/attribute&gt;</td><td>modifiers, type, name, isInit, value, multiplicity</td><td>Define a variable</td></tr><tr><td>&lt;method&gt;&hellip;&lt;/method&gt;</td><td>modifiers, name, returnType</td><td>Define a function</td></tr><tr><td>&lt;constructor&gt;&hellip;&lt;/ constructor &gt;</td><td>modifiers</td><td>Define a class constructor</td></tr><tr><td>&lt;parameter&gt;&hellip;&lt;/parameter&gt;</td><td>name, type, multiplicity</td><td>Define a parameter</td></tr><tr><td>&lt;loop&gt;&hellip;&lt;/loop&gt;</td><td>counter_name, start_from, until, step_size</td><td>Define a loop</td></tr><tr><td>&lt;if&gt;&hellip;&lt;/if&gt;</td><td>condition</td><td>Define a conditional statement</td></tr><tr><td>&lt;initialize&gt;&hellip;&lt;initialize&gt;</td><td>left_side, operator, right_side</td><td>Define an assignment</td></tr><tr><td>&lt;super&gt;&hellip;&lt;/super&gt;</td><td>left_side, operator, right_side</td><td>Call the parent constructor</td></tr><tr><td>&lt;return&gt;&hellip;&lt;/return&gt;</td><td>return</td><td>Return a value from a function</td></tr><tr><td>&lt;call&gt;&hellip;&lt;/call&gt;</td><td>which_object, which_method, argument_list</td><td>Call a function</td></tr><tr><td>&lt;inheritance&gt;&hellip;&lt;/inheritance&gt;</td><td>superClass_id</td><td>Inherit from a concrete class</td></tr><tr><td>&lt;realization&gt;&hellip;&lt;/realization&gt;</td><td>superClass_id</td><td>Inherit from an interface class</td></tr><tr><td>&lt;dependency&gt;&hellip;&lt;/dependency&gt;</td><td>supplier_id</td><td>Dependency between two classes</td></tr><tr><td>&lt;association&gt;&hellip;&lt;/association&gt;</td><td>destination_id, multiplicity</td><td>Association between two classes</td></tr></tbody></table><p><sub>*If the value of this field is True, it means that this role is a main role in the pattern.</sub></p>'},
                 "result": {"title": "Result Section",
                            "content": '<p>In this section, the evaluation results will be analyzed and displayed to '
                                       'the user. The analysis performed on the obtained results includes items such '
                                       'as ranking algorithms registered in the benchmark, as well as displaying some '
                                       'statistical charts.</p><p>Note: In PDB<sub>GTGT</sub>, the evaluation process '
                                       'will be repeated so that the recall metric for the detection method converges '
                                       'to a certain value (if the recall values do not converge, the process '
                                       'iterates 100 times). Therefore, the reported results are the Average, '
                                       'Variance, and Standard deviation of the obtained values in each iteration.</p> '
                            },
                 "compare": {"title": "Comparison Section",
                             "content": '<p>This section allows the user to compare the primary and secondary results '
                                        'including the detected instances as well as the evaluation metrics obtained '
                                        'from different detection algorithms on the same input testbed.</p><p>Note: '
                                        'In PDB<sub>GTGT</sub> the proposed evaluation process is intended to '
                                        'evaluate only one pattern detection method. However, given that the '
                                        'evaluation results are stored along with the test specification, to compare '
                                        'several methods with each other, we only need to consider the same test '
                                        'conditions in the evaluation process. In this regard, we have considered a '
                                        'well-defined and predefined set of testbeds with various levels of '
                                        'complexity as the input of all methods.</p> '
                             },
                 "search": {"title": "Search Section",
                            "content": '<p>This section allows users find the details of the results of a particular '
                                       'detection algorithm, according to different parameters.</p> '
                            },
                 }

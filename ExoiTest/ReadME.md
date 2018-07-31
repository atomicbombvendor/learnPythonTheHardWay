# 如何开始运行GEDF的测试？需要准备哪些的配置？

> 需要配置的地方？
> 总结：两个配置文件`GenerateBat_config.ini`和`AutoTest.ini`。其它的配置文件会自动生成，同时，是新的FileType，则需要在`CompareExoi`中添加相应的代码。

这是具体的介绍:

1. GenerateBat_config.ini文件。这个配置文件是用来在生成两套bat。
   关于GenerateBat_config.ini配置说明：

    1. 根据`root`目录下的bat 生成两套对应的bat;
    2. source_bat和new_branch_bat是两套测试的根目录;
    3. bat_folder 生成文件的bat的目录名, 在两套测试根目录下存放的位置;
    4. source_ZipFile和new_branch_ZipFile同上;
    5. delta_msg msg存放的目录，这里配置了后，代码会自动在配置文件中修改;
    6. FileType bat 中指定的文件类型;
    7. FileName 是用来查找Zip包的文件的,必须和生成文件名一致。
    8. IdList 需要在文件中生成的Id;
    9. Deadwood可以有两套Id同时存在。
    10. 如果FileType和IdList或者IDType为空，则不会替换bat文件中的内容。

    配置了`GenerateBat_config.ini`后，运行GenerateBat.py会生成对应的bat到配置中的目录。
    需要查看怎么去做Delta的测试。

然后，手动运行bat文件。bat文件只用生成一次，就可以多次运行。

2. 配置了`GenerateBat_config.ini`，**生成了Zip文件后**,还需要做什么配置吗？

    不需要了，下面要做的是在`AutoTest.ini`中修改`Section_test`的值，改为需要测试节点。代码会自动扫描`FileName`中配置的Zip包的名字，将相关的Zip包的路径都写入配置文件`CompareExoi_File_Config.ini`和`CompareZip_File_Config.ini`。然后自动的运行。
    如果没有对应的FileType的解析，需要在代码中添加相应的代码，如果没有比较FileType值的代码，需要在`CompareExoi`中添加相应的代码.

3. 对于新的FileType需要在`CompareExoi`添加代码，需要注意什么？
    - 入口程序是ExoiEntry.py. 需要在此文件中增加相应的file_type，方便传入对应的解析类的类型。具体的是在`get_file_types`中添加新的FileType.
    - 添加新的FileType解析类，并在工厂类`EXOITypeFactory`中注册。
    - 如果是新的文件，在master分支可能没有文件可以比对，工具还没有添加相关的功能。

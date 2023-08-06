# Creating custom extensions

## 1. Introduction

Before you start implementing your own extension you will have to think about what kind of extension you want to have.
There is two different abstract classes that your extension can inherit from:

 - FlatExtension
 - NestedExtension (a more advanced FlatExtension)

FlatExtensions are useful for single files or a bunch of files that you want to combine. They will instantly display the Plot (with whatever data you feed it).

NestedExtensions combine FlatExtensions with a FileTree-Widget. This allows the user to more easily browse through, e.g., hierarchical or nested data. Before a Plot is displayed the user will have to select a leaf of the FileTree which can contain arbritary data.

The difference is best explained with two clips: [Video for FlatExtension](https://drive.google.com/file/d/1cXk8lnQBABxSvb1jlFKh79TiAZebE2hr/view) and [Video for NestedExtension](https://drive.google.com/file/d/1gpEwPKQdQ1gpVazHXnax0xl1iIZEzb7t/view?usp=sharing).

Once you have made up your mind check out the next section. 

## 2. Creating a custom extension
In the following the recommended way to create a custom extension is described:
0. Whenever you encounter problems or are not sure what to do check out the example-extensions in the package `pil` which resides in the same folder as this README.
1. Create a subpackage in the same folder as this README.
2. Add a module called `extension.py` to your subpackage.
3. Add a class to your `extension.py` with whatever (valid) name you want, we will call it `MyExt` in the next steps.
Make sure it subclasses either `FlatExtension` or `NestedExtension`
4. Add `__init__.py` to your subpackage and import `MyExt` like so:
   - `from .extension import MyExt`
5. Add the required fields to `MyExt`. Your IDE should give you the option to automatically create the stubs for you or you can Copy&Paste them from any of the already implemented Extensions.
    
    - alias (`str`): 
        - Unique(!) name used for internal representation of your extension
        - Also used to choose an extension if using a JupyterNotebook          
        - Recommended to be short and meaningful
        - Examples: `"mrd"`, `"my_ext"`, or `"someExtName"`
    - file_description (`str`):
        - The name under which your extension is displayed for the user
        - Examples: `"ISMRMRD-files"`, or `"Text-Documents"` 
    - supported_files (`str` or `tuple[str, ...]`)
        - The file-extensions that your extension supports
        - (You can still try to load files without that extension but that will cause errors if the file is not supported)
        - Can be a String or a Tuple of Strings
        - Examples: `"*"`, `"ext"`, `".ext"`, `"*.ext"`, `("h5", ".h6", "*.h7")`
    - multiple (`bool`):
        - Control if only one or multiple files can be selected at once by the user
        - Setting this to `True` will make the filepath class variable of your extension to be a Tuple of filepath-strings
        - Setting this to `False` will make it be a single filepath-string
6. Now you can create the actual logic for `MyExt`. Continue with either Section 2.1 or 2.2.
7. Once you are done with Step 6, import `MyExt` and activate it in `ext_manager.py`.

<a name="FlatExtension"></a>
### 2.1 Creating a custom 'FlatExtension'
Before you start you should check out the extension at [pil/pil_flat](pil/pil_flat) to get a rough understanding of what a FlatExtension can look like.


There's only one function you have to create: `create_plot`.

The How-To is best shown with an example; let's create an extension that takes exactly one path
and creates an image-series. The images' data should be made up of the filepath-string somehow: 
```python

    def create_plot(self, loading_div=None):
        
        # This allows us to print messages to a notebook
        # or a (standalone's) loading screen with the same function
        if loading_div is None:  # invoked from a notebook
            print_msg = print
        else:   # invoked from the standalone app
            print_msg = loading_div.set_text
                
        # Display text while we are "calculating" the plot
        print_msg("I am currently very busy.") 
        time.sleep(3)
        
        # Here we act as if `multiple=False` was set as a class variable
        # so self.path is a string (as opposed to a tuple of strings).        
        # Now: Convert the selected file-path to a list containing its ASCII-equivalent 
        x_axis_values = [ord(c) for c in self.path]    
        
        height = 50
        amount_images = 5
        
        multidim_image = list()
        
        # Create a 3D Image
        for _ in range(amount_images):
            two_dim_image = list()
            for y in range(height):
                x_vals = numpy.roll(x_axis_values, y)  # shift array by y
                two_dim_image.append(x_vals)
            multidim_image.append(two_dim_image)
        
        
        multidim_image = numpy.array(multidim_image)
        
        # The Plot expects to be supplied with a ParsedData object:
        parsed = ParsedData(
            data=multidim_image,
            dim_names=["images", "y", "x"],
            dim_lengths=multidim_image.shape, 
            dim_units=["image", "char", "char"]  # units for the axes
        )
        
        # We return an ImagePlot because our data is not complex
        return ImagePlot(parsed, self.config.image)

        # Check Section 3 for information on what kind of Plots we can display

```

Now try to get a FlatExtension implemented that uses this `create_plot`-function.
Hint: As the file at the user-selected path is not actually read in any way you can set `supported_files = "*"`. Don't forget step 7 from above! 

The solution is located under `examples/example_flat`.

<a name="NestedExtension"></a>
### 2.2 Creating a custom 'NestedExtension'

`NestedExtensions` bring a bit more complexity to the table than `FlatExtensions`
but if you follow these steps it should still be straight forward.

In this exemplary `NestedExtension` we want to handle multiple user-specified filepaths,
create a leaf (in the FileTree-widget) for every filepath and also create a Header containing 
tabular metadata about the selected files:

0. Unlike `FlatExtensions` there's multiple functions that must be implemented here:
   - `get_data_leaves`, `get_tree_structure`, `get_valid_leaf_type_combinations`, and `create_plot`
1. Let's start with `get_tree_structure`:
   - The goal of this function is create a tree-like structure; for this we can use the user-supplied paths,
     the file-content of the paths or anything, really.
      
   - Let's see what it could look like for our example:
   
```python
    @staticmethod
    def get_tree_structure(file_path):

        tree_structure = list()  # a 1d (flat) list to contain the structure of our FileTree
        root_name = f"{len(file_path)} random images"  # Name of the TreeRoot
        # necessary fields for each TreeNode are: "id", "parent", "text", and "type"
        # All fields are required and need to be strings
        root = {"id": "root",  # used to assign children
                "parent": "#", # ID of parent, use "#" for your TreeRoot
                "text": root_name, # Text to be displayed in the FileTree
                "type": "file"}  # Node-Icon, can be "file", "header", "acquisitions", or "images"
        tree_structure.append(root)
        # Creating the header here, as we only need one.
        header = {"id": "header", "parent": "root", "text": "Header", "type": "header"}
        tree_structure.append(header)
        for index, path in enumerate(file_path):
            # Now we iterate over every path and add a corresponding "images"-Node.
            node = {"id": path, "parent": "root", "text": str(index), "type": "images"}
            tree_structure.append(node)
        return tree_structure
```
   Usually some kind of recursion is necessary to fill the tree for nested files, like in the `mrd`-extension.
   This function will automatically be invoked and used to create the FileTree.

2. `get_data_leaves` is used to get data when a leaf of the FileTree is clicked, as we cannot store complex data in the FileTree itself:
```python
    @staticmethod
    def get_data_leaves(file_path):
        data_leaves = dict()
        file_path: tuple  # because we set `multiple=True`
        for path in file_path:
            data_leaves[path] = path  # Let's just use the path as a key and value for the images
        data_leaves["header"] = file_path  # And the header gets a tuple with all paths
        return data_leaves
```
With this implemented we can access `self.data_leaves` in `create_plot`

3. `get_valid_leaf_type_combinations` only has to be implemented if you want to use the extension in a notebook.
There you need it to be able to select different TreeLeaves, as you select them programmatically (by specifying the right key), 
   as opposed to graphically in the standalone:
   
```python
    def get_valid_leaf_type_combinations(self):
        return [name for name in self.data_leaves.keys()]
```

4. Finally we need to be able to actually create Plots; `create_plot`:
```python
    def create_plot(self,
                    leaf_name: str,  # ID of the leaf
                    container_name: str,  # name of the leaf's parent
                    container_type: str,  # type of the leaf
                    loading_div=None):
        # in `get_data_leaves` we specified the keys as the path
        # and in `get_tree_structure` we set a node's ID to their path
        # so we can access `self.data_leaves` like this
        path = self.data_leaves[leaf_name]
        
        # Now we can access the Node's type (as specified in `get_tree_structure`
        # to change the type of Plot we want to display
        if container_type == "header":
            path: tuple   # path is a tuple for the header
            # A TablePlot needs a dict with the column-names as keys
            # and the columns entries as the values
            column_dict = dict(keys=list(), values=list())
            # Let's put in some metadata
            for index, p in enumerate(path):
                column_dict["keys"].append(f"Image{index}'s path")
                column_dict["values"].append(p)
            column_dict["keys"].append("Length of all paths combined")
            comb_length = len("".join(path))
            column_dict["values"].append(comb_length)
            # Feed the Metadata-dict to the TablePlot
            return TablePlot(column_dict)
        else:  # If the type is not 'header' it has to be 'images'
            path: str
            np.random.seed(seed=len(path))  # let's make the image the same for paths with the same length
            data = np.random.rand(2, 4, 3, 34, 35)
            parsed = ParsedData(
                data=data,
                dim_names=["dim4", "dim3", "dim2", "dim1", "dim0"],
                dim_lengths=np.array(data.shape)*2,
                dim_units=["mm", "mm", "mm", "mm", "mm"],
            )
            return ImagePlot(parsed, self.config.image)
```
That's it! For these examples we did not even look into the file's contents (for the sake of simplicity)
but it would obviously be sensible to do so and not use random data for the ImagePlot.

For another example you can check out the nested extension in `pil` or `mrd`.
   

## 3 Displaying different types of Plots

Currently there is 3 different kinds of Plots you can display:
 - `ImagePlot`, to display a multidimensional array of floats/ints
 - `ComplexPlot`, to display a multidimensional array of complex values
 - `TablePlot`, to display (meta)-data in a tabular way

Here's an overview of what kind of data they accept:

### ImagePlot

Accepts a ParsedData-object with non-complex values:

```python
data = np.arange(100).reshape(10, 10)
parsed_data = ParsedData(
   data=data,
   dim_names=["y", "x"],
   dim_lengths=[20, 20],  # one datapoint actually resembles 2 millimeters
   dim_units=["mm", "mm"]
)
image_plot = ImagePlot(parsed_data, ImageConfig())
```
### ComplexPlot

Much like the ImagePlot but with complex values:

```python
data = np.arange(100).reshape(10, 10).view(dtype="complex64")
parsed_data = ParsedData(
   data=data,
   dim_names=["ky", "kx"],
   dim_lengths=data.shape,
   dim_units=["px", "px"]
)
complex_plot = ComplexPlot(parsed_data, ImageConfig())
```
### TablePlot

Accepts a dictionary with column-names as the key and the entries as their value.

Also accepts various keyword-arguments as specified in the Bokeh
[DataTable-docs](https://docs.bokeh.org/en/latest/docs/reference/models/widgets.tables.html#bokeh.models.widgets.tables.DataTable).

```python
table_dict = {
   'first_col': ["row_one", "--row_two_pseudo_child", "row_three"],
   'second_col':["",        "value for child",        "value_asd"],
   'value_col': ["",        "someValue:x-1123",       "val_12312"]     
}
some_kwargs = {"reorderable": False, "selectable": False}
table_plot = TablePlot(table_dict, **some_kwargs)
```

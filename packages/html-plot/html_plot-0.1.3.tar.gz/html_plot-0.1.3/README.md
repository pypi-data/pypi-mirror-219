This package can be used to render Matplotlib plots as HTML objects in
Jupyter, so that they can be placed in HTML tables, downloaded on click,
and more.

# Installation
```bash
pip install html_plot
```

# Examples
```python
import pandas as pd
my_plot = pd.DataFrame([[1,2,3],[4,5,6]]).plot()
```

## Simple usage
```python
html_plot.display(my_plot)
```

## Advanced usage
### Adjust Figure and Axes (e.g. figsize, title)
```python
plot_dim = html_plot.get_dim(my_plot.get_figure())
plot_dim.figsize *= 1.5
ax = html_plot.ax("This is my plot", **plot_dim)
my_html_plot = pd.DataFrame([[1,2,3],[4,5,6]]).plot(ax=ax)
```

### Output HTML string
```python
html_str = html_plot.html_str(my_html_plot)
print(html_str)
```

### Output an `IPython.display.HTML` object
```python
import IPython.display
html_obj = html_plot.HTML(my_html_plot)
IPython.display.display(html_obj)
```

### Display the object using a wrapper for `IPython.display.display()`
```python
html_plot.display(my_html_plot)
```

## Licence

This work is dual-licensed under the [Open Software License 3.0](https://choosealicense.com/licenses/osl-3.0/)
and the [Affero GNU General Public License 3.0](https://choosealicense.com/licenses/agpl-3.0/).
You can choose one of them if you use this work.

`SPDX-License-Identifier: OSL-3.0 OR AGPL-3.0-or-later`

- The primary, more permissive licence is OSL-3.0, which allows the package to
  be used in any software project, regardless of the project's licence (open or
  closed source, commercial or non-commercial).
- If you distribute software that uses a modified version of this package, the
  licence requires you to release **only the code of the modified package**,
  not the whole software project.
- You are very welcome to do the above in the form of pull requests.
- In other words, it's a reasonable, LGPL-like weak copyleft that doesn't try
  to infect all your software with a particular licence.
- See the [explanation and rationale for OSL-3.0](https://rosenlaw.com/OSL3.0-explained.htm)
  written by the author of the licence.
- The alternative licence is AGPL-3.0, which allows the package to be combined
  with GPL-3.0 code.
- Under both OSL-3.0 and AGPL-3.0, the aforementioned weak copyleft is also
  triggered by using the software over a network. In today's age of web apps,
  it makes no sense to have different terms depending on the technical details
  of how the software interacts with the user (locally or over a network). It's
  surprising how few open-source licences have caught up with the times.

Glass Company
-------------
Odoo vertical add-on for running a Glass company sales process.
A module developed by AbAKUS it-solutions

Installation notes
------------------
- Odoo v 9c fix for handling Chrome browser:

We have to change the code of <code>transcoder.js</code> located in <code>web_editor/static/src/js</code>:

The property "rules" is not well checked.

This line is wrong (around line number 16):

<code>if (sheets[i].rules) {</code>

It has to be changed to this:

<code>if (sheets[i].hasOwnProperty('rules')) {</code>

- Third party add-ons:

OCA web_tree_image: <link>https://www.odoo.com/apps/modules/9.0/web_tree_image/</link>
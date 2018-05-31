=====================================
   Glass Company
=====================================

This module is a vertical addon to ``sale``.
It allows running a full glass product company sales process.
It also allow managing glass product settings including:

- finishes

- internal grids

- spacers

- shapes

- generic extras

Installation notes
==================
- Odoo v 9c fix for handling Chrome browser:

We have to change the code of ``transcoder.js`` located in ``web_editor/static/src/js``:

The property "rules" is not well checked.

This line is wrong (around line number 16):

.. code:: javascript
   if (sheets[i].rules) {

It has to be changed to this:

.. code:: javascript
   if (sheets[i].hasOwnProperty('rules')) {

- Third party add-ons:

OCA web_tree_image: 'https://www.odoo.com/apps/modules/9.0/web_tree_image/'

Credits
=======

Contributors
------------

* Jason Pindat
* Valentin Thirion <valentin.thirion@abakusitsolutions.eu>
* Paul Ntabuye Butera <paul.n.butera@abakusitsolutions.eu>

Maintainer
-----------

.. image:: http://www.abakusitsolutions.eu/wp-content/themes/abakus/images/logo.gif
   :alt: AbAKUS IT SOLUTIONS
   :target: http://www.abakusitsolutions.eu

This module is maintained by AbAKUS IT SOLUTIONS
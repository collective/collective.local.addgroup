Introduction
============

Allows to create a group and assign roles directly from the sharing tab for Plone 4.
Tested on Plone 4.1.

Content types have just to implement IAddNewGroup.

Add to the configure.zcml of your policy module::

  <include package="collective.local.addgroup" />
  <class class="my.package.content.MyContent.MyContent">
     <implements interface="collective.local.addgroup.interfaces.IAddNewGroup" />
  </class>

The user need to have the "Add Groups" permission to add a new group and
"Manager users" to add and remove users from the listed groups.

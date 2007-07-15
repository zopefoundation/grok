This is a version of the classic app used to demonstrate a tree data structure.
It is a hierarchical database of animals arranged by distinguishing questions.
Initially, it knows only one animal. But as users interact with it, it learns
more.

This example has a grok.Container subclass called Node. Leaf nodes are empty and
contain the name of one animal. Branch nodes contain a question and two
sub-nodes named 'yes' and 'no'.

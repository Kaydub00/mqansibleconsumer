# mqansibleconsumer
Framework for creating ActiveMQ/RabbitMQ consumers the run Ansible jobs


This is just the basic skeleton structure of something I created to consume a queue for Ansible playbook jobs.

I'd like to start working on making this a bit more configurable/abstract so it can be used by more people. 

The current configuration of the consumer is setup for JMS(Java) messages. It is probably easiest to setup the consumer for String messages. I prefer to put objects into the queue since I usually need more info than just the fqdn. I'll start to add different examples for the different message types soon.

So for this to work the user running the consumer needs to have an ssh key and auth to perform the actions in the playbook on the specified servers. I usually have an ansible user that will run the consumers.

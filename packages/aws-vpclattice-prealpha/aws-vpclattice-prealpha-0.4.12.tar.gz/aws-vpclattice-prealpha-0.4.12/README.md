# aws-vpclattice-prealpha

# vpcLattice L2 Construct

* [Project Information](#project-information)
* [Example Impleentation](#example-implementation)
* [API Design](#proposed-api-design-for-vpclattice)
* [FAQ](#faq)
* [Acceptance](#acceptance)

---


## Project Information

**Status** (DRAFT)

**Original Author(s):** @mrpackethead, , @taylaand,  @nbaillie

**Tracking Issue:** #502

**API Bar Raiser:** @TheRealAmazonKendra

**Public Issues ( aws-cdk)**

* (vpclattice): L2 for Amazon VPC Lattice #25452

**Prototype Code**

* https://github.com/raindancers/aws-cdk/tree/mrpackethead/aws-vpclattice-alpha/packages/%40aws-cdk/aws-vpclattice-alpha

**Example implementation**

* https://github.com/raindancers/vpclattice-prealpha-demo

**Blog**

**VpcLattice**

Amazon VPC Lattice is an application networking service that consistently connects, monitors, and secures communications between your services, helping to improve productivity so that your developers can focus on building features that matter to your business. You can define policies for network traffic management, access, and monitoring to connect compute services in a simplified and consistent way across instances, containers, and serverless applications.

The L2 Construct seeks to assist the consumer to create a lattice service easily by abstracting some of the detail.  The major part of this is in creating the underlying auth policy and listener rules together, as their is significant intersection in the properties require for both.

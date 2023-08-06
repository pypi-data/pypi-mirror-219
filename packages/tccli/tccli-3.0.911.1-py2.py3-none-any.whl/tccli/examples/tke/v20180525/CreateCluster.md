**Example 1: 创建托管集群示例**

创建托管集群

Input: 

```
tccli tke CreateCluster --cli-unfold-argument  \
    --ClusterCIDRSettings.ServiceCIDR xx \
    --ClusterCIDRSettings.ClaimExpiredSeconds 0 \
    --ClusterCIDRSettings.MaxClusterServiceNum 1 \
    --ClusterCIDRSettings.MaxNodePodNum 1 \
    --ClusterCIDRSettings.EniSubnetIds xx \
    --ClusterCIDRSettings.ClusterCIDR xx \
    --ClusterCIDRSettings.IgnoreServiceCIDRConflict True \
    --ClusterCIDRSettings.IgnoreClusterCIDRConflict True \
    --ClusterAdvancedSettings.AuditEnabled True \
    --ClusterAdvancedSettings.DeletionProtection True \
    --ClusterAdvancedSettings.RuntimeVersion xx \
    --ClusterAdvancedSettings.IsDualStack True \
    --ClusterAdvancedSettings.IsNonStaticIpMode True \
    --ClusterAdvancedSettings.KubeProxyMode xx \
    --ClusterAdvancedSettings.AuditLogTopicId xx \
    --ClusterAdvancedSettings.ExtraArgs.KubeAPIServer xx \
    --ClusterAdvancedSettings.ExtraArgs.KubeScheduler xx \
    --ClusterAdvancedSettings.ExtraArgs.KubeControllerManager xx \
    --ClusterAdvancedSettings.ExtraArgs.Etcd xx \
    --ClusterAdvancedSettings.AuditLogsetId xx \
    --ClusterAdvancedSettings.EnableCustomizedPodCIDR True \
    --ClusterAdvancedSettings.CiliumMode xx \
    --ClusterAdvancedSettings.AsEnabled True \
    --ClusterAdvancedSettings.ContainerRuntime xx \
    --ClusterAdvancedSettings.VpcCniType xx \
    --ClusterAdvancedSettings.NetworkType xx \
    --ClusterAdvancedSettings.NodeNameType xx \
    --ClusterAdvancedSettings.IPVS True \
    --ClusterAdvancedSettings.BasePodNumber 0 \
    --ClusterBasicSettings.AutoUpgradeClusterLevel.IsAutoUpgrade True \
    --ClusterBasicSettings.VpcId xx \
    --ClusterBasicSettings.ClusterVersion xx \
    --ClusterBasicSettings.TagSpecification.0.ResourceType xx \
    --ClusterBasicSettings.TagSpecification.0.Tags.0.Value xx \
    --ClusterBasicSettings.TagSpecification.0.Tags.0.Key xx \
    --ClusterBasicSettings.ClusterName xx \
    --ClusterBasicSettings.ProjectId 0 \
    --ClusterBasicSettings.ClusterDescription xx \
    --ClusterBasicSettings.NeedWorkSecurityGroup True \
    --ClusterBasicSettings.SubnetId xx \
    --ClusterBasicSettings.OsCustomizeType xx \
    --ClusterBasicSettings.ClusterLevel xx \
    --ClusterBasicSettings.ClusterOs xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.PreStartUserScript xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DockerGraphPath xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.Labels.0.Name xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.Labels.0.Value xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.ExtraArgs.Kubelet xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.Taints.0.Value xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.Taints.0.Key xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.Taints.0.Effect xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.Unschedulable 0 \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.UserScript xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DesiredPodNumber 0 \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.MIGEnable True \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.CustomDriver.Address xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.Driver.Version xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.Driver.Name xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.CUDA.Version xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.CUDA.Name xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.CUDNN.DocName xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.CUDNN.Version xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.CUDNN.Name xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.GPUArgs.CUDNN.DevName xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.MountTarget xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DataDisks.0.DiskPartition xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DataDisks.0.DiskType xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DataDisks.0.DiskSize 0 \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DataDisks.0.FileSystem xx \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DataDisks.0.AutoFormatAndMount True \
    --RunInstancesForNode.0.InstanceAdvancedSettingsOverrides.0.DataDisks.0.MountTarget xx \
    --RunInstancesForNode.0.NodeRole xx \
    --RunInstancesForNode.0.RunInstancesPara {"VirtualPrivateCloud":{"SubnetId":"subnet-xxx","VpcId":"vpc-xxx"},"Placement":{"Zone":"ap-region-1","ProjectId":1032509},"InstanceType":"S3.LARGE8","SystemDisk":{"DiskType":"CLOUD_PREMIUM"},"DataDisks":[{"DiskType":"CLOUD_PREMIUM","DiskSize":50}],"InstanceCount":1,"InternetAccessible":{"PublicIpAssigned":true,"InternetMaxBandwidthOut":1},"LoginSettings":{"Password":"YourPassword"},"UserData":"IyEvYmluL3NoCgplY2hvIGFhYQo="} \
    --ExtensionAddons.0.AddonName xx \
    --ExtensionAddons.0.AddonParam xx \
    --ClusterType xx \
    --InstanceAdvancedSettings.PreStartUserScript xx \
    --InstanceAdvancedSettings.DockerGraphPath xx \
    --InstanceAdvancedSettings.Labels.0.Name xx \
    --InstanceAdvancedSettings.Labels.0.Value xx \
    --InstanceAdvancedSettings.ExtraArgs.Kubelet xx \
    --InstanceAdvancedSettings.Taints.0.Value xx \
    --InstanceAdvancedSettings.Taints.0.Key xx \
    --InstanceAdvancedSettings.Taints.0.Effect xx \
    --InstanceAdvancedSettings.Unschedulable 0 \
    --InstanceAdvancedSettings.UserScript xx \
    --InstanceAdvancedSettings.DesiredPodNumber 0 \
    --InstanceAdvancedSettings.GPUArgs.MIGEnable True \
    --InstanceAdvancedSettings.GPUArgs.CustomDriver.Address xx \
    --InstanceAdvancedSettings.GPUArgs.Driver.Version xx \
    --InstanceAdvancedSettings.GPUArgs.Driver.Name xx \
    --InstanceAdvancedSettings.GPUArgs.CUDNN.DocName xx \
    --InstanceAdvancedSettings.GPUArgs.CUDNN.Version xx \
    --InstanceAdvancedSettings.GPUArgs.CUDNN.Name xx \
    --InstanceAdvancedSettings.GPUArgs.CUDNN.DevName xx \
    --InstanceAdvancedSettings.MountTarget xx \
    --InstanceAdvancedSettings.DataDisks.0.DiskPartition xx \
    --InstanceAdvancedSettings.DataDisks.0.DiskType xx \
    --InstanceAdvancedSettings.DataDisks.0.DiskSize 0 \
    --InstanceAdvancedSettings.DataDisks.0.FileSystem xx \
    --InstanceAdvancedSettings.DataDisks.0.AutoFormatAndMount True \
    --InstanceAdvancedSettings.DataDisks.0.MountTarget xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.PreStartUserScript xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DockerGraphPath xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.Labels.0.Name xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.Labels.0.Value xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.ExtraArgs.Kubelet xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.Taints.0.Value xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.Taints.0.Key xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.Taints.0.Effect xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.Unschedulable 0 \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.UserScript xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DesiredPodNumber 0 \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.GPUArgs.MIGEnable True \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.GPUArgs.CustomDriver.Address xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.GPUArgs.CUDNN.DocName xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.GPUArgs.CUDNN.Version xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.GPUArgs.CUDNN.Name xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.GPUArgs.CUDNN.DevName xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.MountTarget xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DataDisks.0.DiskPartition xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DataDisks.0.DiskType xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DataDisks.0.DiskSize 0 \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DataDisks.0.FileSystem xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DataDisks.0.AutoFormatAndMount True \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceAdvancedSettings.DataDisks.0.MountTarget xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.HostName xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.LoginSettings.Password xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.LoginSettings.KeepImageLogin xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.LoginSettings.KeyIds xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.SecurityGroupIds xx \
    --ExistedInstancesForNode.0.ExistedInstancesPara.EnhancedService.SecurityService.Enabled True \
    --ExistedInstancesForNode.0.ExistedInstancesPara.EnhancedService.MonitorService.Enabled True \
    --ExistedInstancesForNode.0.ExistedInstancesPara.EnhancedService.AutomationService.Enabled True \
    --ExistedInstancesForNode.0.ExistedInstancesPara.InstanceIds xx \
    --ExistedInstancesForNode.0.DesiredPodNumbers 0 \
    --ExistedInstancesForNode.0.NodeRole xx \
    --InstanceDataDiskMountSettings.0.InstanceType xx \
    --InstanceDataDiskMountSettings.0.Zone xx \
    --InstanceDataDiskMountSettings.0.DataDisks.0.DiskPartition xx \
    --InstanceDataDiskMountSettings.0.DataDisks.0.DiskType xx \
    --InstanceDataDiskMountSettings.0.DataDisks.0.DiskSize 0 \
    --InstanceDataDiskMountSettings.0.DataDisks.0.FileSystem xx \
    --InstanceDataDiskMountSettings.0.DataDisks.0.AutoFormatAndMount True \
    --InstanceDataDiskMountSettings.0.DataDisks.0.MountTarget xx
```

Output: 
```
{
    "Response": {
        "ClusterId": "cls-xxx",
        "RequestId": "eac6b301-a322-493a-8e36-83b295459397"
    }
}
```

**Example 2: 创建独立集群示例**

创建独立集群

Input: 

```
tccli tke CreateCluster --cli-unfold-argument  \
    --ClusterType INDEPENDENT_CLUSTER \
    --ClusterCIDRSettings.ClusterCIDR 10.4.0.0/14 \
    --RunInstancesForNode.0.NodeRole MASTER_ETCD \
    --RunInstancesForNode.0.RunInstancesPara {"VirtualPrivateCloud":{"SubnetId":"subnet-xxx","VpcId":"vpc-xxx"},"Placement":{"Zone":"ap-region-1","ProjectId":1032509},"InstanceType":"S3.LARGE8","SystemDisk":{"DiskType":"CLOUD_PREMIUM"},"DataDisks":[{"DiskType":"CLOUD_PREMIUM","DiskSize":50}],"InstanceCount":3,"InternetAccessible":{"PublicIpAssigned":true,"InternetMaxBandwidthOut":1},"LoginSettings":{"Password":"YourPassword"},"UserData":"IyEvYmluL3NoCgplY2hvIGFhYQo \
    --RunInstancesForNode.1.NodeRole WORKER \
    --RunInstancesForNode.1.RunInstancesPara {"VirtualPrivateCloud":{"SubnetId":"subnet-xxx","VpcId":"vpc-xxx"},"Placement":{"Zone":"ap-region-1","ProjectId":1032509},"InstanceType":"S3.LARGE8","SystemDisk":{"DiskType":"CLOUD_PREMIUM"},"DataDisks":[{"DiskType":"CLOUD_PREMIUM","DiskSize":50}],"InstanceCount":1,"InternetAccessible":{"PublicIpAssigned":true,"InternetMaxBandwidthOut":1},"LoginSettings":{"Password":"YourPassword"},"UserData":"IyEvYmluL3NoCgplY2hvIGFhYQo \
    --ExtensionAddons.0.AddonName GameApp \
    --ExtensionAddons.0.AddonParam {"kind":"GameApp","apiVersion":"platform.tke/v1","metadata":{"generateName":"ga"},"spec":{"clusterName":"xxx"}}
```

Output: 
```
{
    "Response": {
        "ClusterId": "cls-xxx",
        "RequestId": "eac6b301-a322-493a-8e36-83b295459397"
    }
}
```


import pygltflib

# 读取GLB文件
glb_file_path = "../data/zqf.glb"
glb = pygltflib.GLTF2().load(glb_file_path)

# 获取场景
scene = glb.scenes[0]

# 获取场景中所有节点的位置信息
positions = []
for node_idx in scene.nodes:
    node = glb.nodes[node_idx]
    if node.mesh is not None:
        mesh = glb.meshes[node.mesh]
        for primitive in mesh.primitives:
            accessor_idx = primitive.attributes.POSITION
            accessor = glb.accessors[accessor_idx]
            buffer_view = glb.buffer_views[accessor.buffer_view]
            buffer = glb.buffer_views[buffer_view.buffer]
            position_data = buffer.data[buffer_view.byte_offset + accessor.byte_offset: buffer_view.byte_offset + accessor.byte_offset + accessor.count * accessor.data_type.itemsize]
            positions.extend(position_data)

# 计算几何中心
x_values = positions[::3]
y_values = positions[1::3]
z_values = positions[2::3]
center_x = sum(x_values) / len(x_values)
center_y = sum(y_values) / len(y_values)
center_z = sum(z_values) / len(z_values)

print("物体几何中心坐标：")
print("X坐标：", center_x)
print("Y坐标：", center_y)
print("Z坐标：", center_z)


import nibabel as nib

# 读取NIfTI文件
nifti_file_path = "../data/zqf.nii.gz"
nifti_image = nib.load(nifti_file_path)

origin = nifti_image.affine[:3, 3]

print("CT原点位置：")
print("X坐标：", origin[0])
print("Y坐标：", origin[1])
print("Z坐标：", origin[2])
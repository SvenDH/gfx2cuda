import ctypes
import ctypes.wintypes as wintypes

import comtypes


class DXGI_SAMPLE_DESC(ctypes.Structure):
    _fields_ = [
        ("Count", wintypes.UINT),
        ("Quality", wintypes.UINT),
    ]


class D3D11_BOX(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.UINT),
        ("top", wintypes.UINT),
        ("front", wintypes.UINT),
        ("right", wintypes.UINT),
        ("bottom", wintypes.UINT),
        ("back", wintypes.UINT),
    ]


class D3D11_TEXTURE2D_DESC(ctypes.Structure):
    _fields_ = [
        ("Width", wintypes.UINT),
        ("Height", wintypes.UINT),
        ("MipLevels", wintypes.UINT),
        ("ArraySize", wintypes.UINT),
        ("Format", wintypes.UINT),
        ("SampleDesc", DXGI_SAMPLE_DESC),
        ("Usage", wintypes.UINT),
        ("BindFlags", wintypes.UINT),
        ("CPUAccessFlags", wintypes.UINT),
        ("MiscFlags", wintypes.UINT),
    ]


class D3D11_MAPPED_SUBRESOURCE(ctypes.Structure):
    _fields_ = [
        ("pData", ctypes.c_void_p),
        ("RowPitch", wintypes.UINT),
        ("DepthPitch", wintypes.UINT),
    ]


class ID3D11DeviceChild(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{1841e5c8-16b0-489b-bcc8-44cfb0d5deae}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDevice"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetPrivateData"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateData"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateDataInterface"),
    ]


class ID3D11Resource(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{dc8e63f3-d12b-4952-b47b-5e45026a862d}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetType"),
        comtypes.STDMETHOD(None, "SetEvictionPriority"),
        comtypes.STDMETHOD(wintypes.UINT, "GetEvictionPriority"),
    ]


class ID3D11Texture2D(ID3D11Resource):
    _iid_ = comtypes.GUID("{6f15aaf2-d208-4e89-9ab4-489535d34f9c}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc", [ctypes.POINTER(D3D11_TEXTURE2D_DESC)]),
    ]


class ID3D11View(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{839d1216-bb2e-412b-b7f4-a9dbebe08ed1}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetResource"),
    ]


class ID3D11RenderTargetView(ID3D11View):
    _iid_ = comtypes.GUID("{dfdba067-0b8d-4865-875b-d7b4516cc164}")
    _methods_ = [
        comtypes.STDMETHOD(None, "GetDesc"),
    ]


class ID3D11DeviceContext(ID3D11DeviceChild):
    _iid_ = comtypes.GUID("{c0bfa96c-e089-44fb-8eaf-26f8796190da}")
    _methods_ = [
        comtypes.STDMETHOD(None, "VSSetConstantBuffers"),
        comtypes.STDMETHOD(None, "PSSetShaderResources"),
        comtypes.STDMETHOD(None, "PSSetShader"),
        comtypes.STDMETHOD(None, "PSSetSamplers"),
        comtypes.STDMETHOD(None, "VSSetShader"),
        comtypes.STDMETHOD(None, "DrawIndexed"),
        comtypes.STDMETHOD(None, "Draw"),
        comtypes.STDMETHOD(comtypes.HRESULT, "Map"),
        comtypes.STDMETHOD(None, "Unmap"),
        comtypes.STDMETHOD(None, "PSSetConstantBuffers"),
        comtypes.STDMETHOD(None, "IASetInputLayout"),
        comtypes.STDMETHOD(None, "IASetVertexBuffers"),
        comtypes.STDMETHOD(None, "IASetIndexBuffer"),
        comtypes.STDMETHOD(None, "DrawIndexedInstanced"),
        comtypes.STDMETHOD(None, "DrawInstanced"),
        comtypes.STDMETHOD(None, "GSSetConstantBuffers"),
        comtypes.STDMETHOD(None, "GSSetShader"),
        comtypes.STDMETHOD(None, "IASetPrimitiveTopology"),
        comtypes.STDMETHOD(None, "VSSetShaderResources"),
        comtypes.STDMETHOD(None, "VSSetSamplers"),
        comtypes.STDMETHOD(None, "Begin"),
        comtypes.STDMETHOD(None, "End"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetData"),
        comtypes.STDMETHOD(None, "SetPredication"),
        comtypes.STDMETHOD(None, "GSSetShaderResources"),
        comtypes.STDMETHOD(None, "GSSetSamplers"),
        comtypes.STDMETHOD(None, "OMSetRenderTargets"),
        comtypes.STDMETHOD(None, "OMSetRenderTargetsAndUnorderedAccessViews"),
        comtypes.STDMETHOD(None, "OMSetBlendState"),
        comtypes.STDMETHOD(None, "OMSetDepthStencilState"),
        comtypes.STDMETHOD(None, "SOSetTargets"),
        comtypes.STDMETHOD(None, "DrawAuto"),
        comtypes.STDMETHOD(None, "DrawIndexedInstancedIndirect"),
        comtypes.STDMETHOD(None, "DrawInstancedIndirect"),
        comtypes.STDMETHOD(None, "Dispatch"),
        comtypes.STDMETHOD(None, "DispatchIndirect"),
        comtypes.STDMETHOD(None, "RSSetState"),
        comtypes.STDMETHOD(None, "RSSetViewports"),
        comtypes.STDMETHOD(None, "RSSetScissorRects"),
        comtypes.STDMETHOD(
            None,
            "CopySubresourceRegion",
            [
                ctypes.POINTER(ID3D11Resource),
                wintypes.UINT,
                wintypes.UINT,
                wintypes.UINT,
                wintypes.UINT,
                ctypes.POINTER(ID3D11Resource),
                wintypes.UINT,
                ctypes.POINTER(D3D11_BOX),
            ],
        ),
        comtypes.STDMETHOD(
            None, "CopyResource", [ctypes.POINTER(ID3D11Resource), ctypes.POINTER(ID3D11Resource)],
        ),
        comtypes.STDMETHOD(None, "UpdateSubresource"),
        comtypes.STDMETHOD(None, "CopyStructureCount"),
        comtypes.STDMETHOD(None, "ClearRenderTargetView", [
            ctypes.POINTER(ID3D11RenderTargetView),
            ctypes.c_float * 4,
        ]),
        comtypes.STDMETHOD(None, "ClearUnorderedAccessViewUint"),
        comtypes.STDMETHOD(None, "ClearUnorderedAccessViewFloat"),
        comtypes.STDMETHOD(None, "ClearDepthStencilView"),
        comtypes.STDMETHOD(None, "GenerateMips"),
        comtypes.STDMETHOD(None, "SetResourceMinLOD"),
        comtypes.STDMETHOD(wintypes.FLOAT, "GetResourceMinLOD"),
        comtypes.STDMETHOD(None, "ResolveSubresource"),
        comtypes.STDMETHOD(None, "ExecuteCommandList"),
        comtypes.STDMETHOD(None, "HSSetShaderResources"),
        comtypes.STDMETHOD(None, "HSSetShader"),
        comtypes.STDMETHOD(None, "HSSetSamplers"),
        comtypes.STDMETHOD(None, "HSSetConstantBuffers"),
        comtypes.STDMETHOD(None, "DSSetShaderResources"),
        comtypes.STDMETHOD(None, "DSSetShader"),
        comtypes.STDMETHOD(None, "DSSetSamplers"),
        comtypes.STDMETHOD(None, "DSSetConstantBuffers"),
        comtypes.STDMETHOD(None, "CSSetShaderResources"),
        comtypes.STDMETHOD(None, "CSSetUnorderedAccessViews"),
        comtypes.STDMETHOD(None, "CSSetShader"),
        comtypes.STDMETHOD(None, "CSSetSamplers"),
        comtypes.STDMETHOD(None, "CSSetConstantBuffers"),
        comtypes.STDMETHOD(None, "VSGetConstantBuffers"),
        comtypes.STDMETHOD(None, "PSGetShaderResources"),
        comtypes.STDMETHOD(None, "PSGetShader"),
        comtypes.STDMETHOD(None, "PSGetSamplers"),
        comtypes.STDMETHOD(None, "VSGetShader"),
        comtypes.STDMETHOD(None, "PSGetConstantBuffers"),
        comtypes.STDMETHOD(None, "IAGetInputLayout"),
        comtypes.STDMETHOD(None, "IAGetVertexBuffers"),
        comtypes.STDMETHOD(None, "IAGetIndexBuffer"),
        comtypes.STDMETHOD(None, "GSGetConstantBuffers"),
        comtypes.STDMETHOD(None, "GSGetShader"),
        comtypes.STDMETHOD(None, "IAGetPrimitiveTopology"),
        comtypes.STDMETHOD(None, "VSGetShaderResources"),
        comtypes.STDMETHOD(None, "VSGetSamplers"),
        comtypes.STDMETHOD(None, "GetPredication"),
        comtypes.STDMETHOD(None, "GSGetShaderResources"),
        comtypes.STDMETHOD(None, "GSGetSamplers"),
        comtypes.STDMETHOD(None, "OMGetRenderTargets"),
        comtypes.STDMETHOD(None, "OMGetRenderTargetsAndUnorderedAccessViews"),
        comtypes.STDMETHOD(None, "OMGetBlendState"),
        comtypes.STDMETHOD(None, "OMGetDepthStencilState"),
        comtypes.STDMETHOD(None, "SOGetTargets"),
        comtypes.STDMETHOD(None, "RSGetState"),
        comtypes.STDMETHOD(None, "RSGetViewports"),
        comtypes.STDMETHOD(None, "RSGetScissorRects"),
        comtypes.STDMETHOD(None, "HSGetShaderResources"),
        comtypes.STDMETHOD(None, "HSGetShader"),
        comtypes.STDMETHOD(None, "HSGetSamplers"),
        comtypes.STDMETHOD(None, "HSGetConstantBuffers"),
        comtypes.STDMETHOD(None, "DSGetShaderResources"),
        comtypes.STDMETHOD(None, "DSGetShader"),
        comtypes.STDMETHOD(None, "DSGetSamplers"),
        comtypes.STDMETHOD(None, "DSGetConstantBuffers"),
        comtypes.STDMETHOD(None, "CSGetShaderResources"),
        comtypes.STDMETHOD(None, "CSGetUnorderedAccessViews"),
        comtypes.STDMETHOD(None, "CSGetShader"),
        comtypes.STDMETHOD(None, "CSGetSamplers"),
        comtypes.STDMETHOD(None, "CSGetConstantBuffers"),
        comtypes.STDMETHOD(None, "ClearState"),
        comtypes.STDMETHOD(None, "Flush"),
        comtypes.STDMETHOD(None, "GetType"),
        comtypes.STDMETHOD(wintypes.UINT, "GetContextFlags"),
        comtypes.STDMETHOD(comtypes.HRESULT, "FinishCommandList"),
    ]


class ID3D11Device(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{db6f6ddb-ac77-4e88-8253-819df9bbf140}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateBuffer"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateTexture1D"),
        comtypes.STDMETHOD(
            comtypes.HRESULT,
            "CreateTexture2D",
            [
                ctypes.POINTER(D3D11_TEXTURE2D_DESC),
                ctypes.POINTER(None),
                ctypes.POINTER(ctypes.POINTER(ID3D11Texture2D)),
            ],
        ),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateTexture3D"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateShaderResourceView"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateUnorderedAccessView"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateRenderTargetView", [
            ctypes.POINTER(ID3D11Resource),
            ctypes.POINTER(None),
            ctypes.POINTER(ctypes.POINTER(ID3D11RenderTargetView)),
        ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDepthStencilView"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateInputLayout"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateVertexShader"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateGeometryShader"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateGeometryShaderWithStreamOutput"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreatePixelShader"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateHullShader"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDomainShader"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateComputeShader"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateClassLinkage"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateBlendState"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDepthStencilState"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateRasterizerState"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSamplerState"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateQuery"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreatePredicate"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateCounter"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateDeferredContext"),
        comtypes.STDMETHOD(comtypes.HRESULT, "OpenSharedResource", [
            wintypes.HANDLE,
            ctypes.POINTER(comtypes.GUID),
            ctypes.POINTER(ctypes.c_void_p),
        ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckFormatSupport"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckMultisampleQualityLevels"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckCounterInfo"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckCounter"),
        comtypes.STDMETHOD(comtypes.HRESULT, "CheckFeatureSupport"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetPrivateData"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateData"),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetPrivateDataInterface"),
        comtypes.STDMETHOD(ctypes.c_int32, "GetFeatureLevel"),
        comtypes.STDMETHOD(ctypes.c_uint, "GetCreationFlags"),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDeviceRemovedReason"),
        comtypes.STDMETHOD(
            None, "GetImmediateContext", [ctypes.POINTER(ctypes.POINTER(ID3D11DeviceContext))],
        ),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetExceptionMode"),
        comtypes.STDMETHOD(ctypes.c_uint, "GetExceptionMode"),
    ]


def d3d_initialize_device(adapter):
    feature_levels = [45312, 45056, 41216, 40960, 37632, 37376, 37120]

    d3d_device = ctypes.POINTER(ID3D11Device)()
    d3d_device_context = ctypes.POINTER(ID3D11DeviceContext)()

    ctypes.windll.d3d11.D3D11CreateDevice(
        adapter,
        0,
        None,
        0,
        ctypes.byref((ctypes.c_uint * 7)(*feature_levels)),
        len(feature_levels),
        7,
        ctypes.byref(d3d_device),
        None,
        ctypes.byref(d3d_device_context),
    )
    return d3d_device, d3d_device_context


def d3d11_flush(d3d_device_context):
    d3d_device_context.Flush()


def d3d11_create_texture_2d(width, height, d3d_device, fmt, cpu_access):
    texture_desc = D3D11_TEXTURE2D_DESC()

    texture_desc.Width = width
    texture_desc.Height = height
    texture_desc.MipLevels = 1
    texture_desc.ArraySize = 1
    texture_desc.SampleDesc.Count = 1
    texture_desc.SampleDesc.Quality = 0
    texture_desc.Usage = 0  # D3D11_USAGE_DEFAULT,
    texture_desc.Format = fmt
    texture_desc.BindFlags = 32  # D3D11_BIND_RENDER_TARGET
    # texture_desc.BindFlags = 8  # D3D11_BIND_SHADER_RESOURCE
    # texture_desc.BindFlags = 32 | 8  # D3D11_BIND_RENDER_TARGET | D3D11_BIND_SHADER_RESOURCE
    if cpu_access:
        texture_desc.CPUAccessFlags = 65536 | 131072  # D3D11_CPU_ACCESS_WRITE|D3D11_CPU_ACCESS_READ
    # texture_desc.CPUAccessFlags = 131072  # D3D11_CPU_ACCESS_READ
    # texture_desc.MiscFlags = 2048  # D3D11_RESOURCE_MISC_SHARED_NTHANDLE
    # texture_desc.MiscFlags = 256  # D3D11_RESOURCE_MISC_SHARED_KEYEDMUTEX
    texture_desc.MiscFlags = 2  # D3D11_RESOURCE_MISC_SHARED

    d3d11_texture = ctypes.POINTER(ID3D11Texture2D)()
    d3d_device.CreateTexture2D(ctypes.byref(texture_desc), None, ctypes.byref(d3d11_texture))
    return d3d11_texture


def d3d11_texture_desc(d3d11_texture):
    d3d11_texture_description = D3D11_TEXTURE2D_DESC()
    d3d11_texture.GetDesc(ctypes.byref(d3d11_texture_description))

    return d3d11_texture_description.Width, d3d11_texture_description.Height, d3d11_texture_description.Format


def d3d11_open_shared_handle(handle, d3d_device):
    resource = ctypes.POINTER(ID3D11Texture2D)()
    d3d_device.OpenSharedResource(handle, ID3D11Texture2D._iid_, ctypes.byref(resource))
    return resource


def d3d11_create_render_target_view(d3d11_texture, d3d_device):
    d3d11_rt = ctypes.POINTER(ID3D11RenderTargetView)()
    d3d_device.CreateRenderTargetView(d3d11_texture, None, ctypes.byref(d3d11_rt))
    return d3d11_rt


def d3d11_clear_render_target(d3d11_rt, d3d_context, r, g, b, a):
    color = (ctypes.c_float * 4)(r, g, b, a)
    d3d_context.ClearRenderTargetView(d3d11_rt, color)
